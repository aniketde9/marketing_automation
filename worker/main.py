import asyncio
import logging
import os
from contextlib import asynccontextmanager, suppress
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI

from db import Database
from gemini_generator import GeminiGenerator
from models import WorkerHealth
from prompts import PROMPT_TEMPLATES, get_content_type_key
from prompt_handler import PromptHandler

# Load environment variables from .env file FIRST
# This ensures all environment variables are loaded before any module uses them
load_dotenv(override=True)  # override=True ensures .env values take precedence over system env vars

# Setup logging AFTER loading .env
logger = logging.getLogger('worker')
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s | %(levelname)s | %(message)s',
)

processed_jobs = 0
last_job_id: Optional[str] = None
stop_event: Optional[asyncio.Event] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global stop_event  # noqa: PLW0603
    
    # Log configuration ONCE at startup (from .env file)
    logger.info("🔧 Configuration loaded from .env:")
    logger.info(f"   GEMINI_MODEL: {os.getenv('GEMINI_MODEL', 'gemini-pro')}")
    logger.info(f"   GEMINI_RPM: {os.getenv('GEMINI_RPM', '2')}")
    logger.info(f"   GEMINI_RPD: {os.getenv('GEMINI_RPD', '50')}")
    logger.info(f"   POLL_INTERVAL: {os.getenv('POLL_INTERVAL', '10')}")
    logger.info("🚀 Worker started, polling every %d seconds", int(os.getenv('POLL_INTERVAL', '10')))
    
    stop_event = asyncio.Event()
    worker_task = asyncio.create_task(job_processor(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        worker_task.cancel()
        with suppress(asyncio.CancelledError):
            await worker_task


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def root():
    return {'service': 'marketing-automation-worker'}


@app.get('/health', response_model=WorkerHealth)
async def health() -> WorkerHealth:
    return WorkerHealth(
        status='healthy',
        processed_jobs=processed_jobs,
        last_job_id=last_job_id,
    )


async def job_processor(event: asyncio.Event):
    global processed_jobs, last_job_id  # noqa: PLW0603
    db = Database()
    poll_interval = int(os.getenv('POLL_INTERVAL', '10'))

    logger.info("📋 Worker loop started, waiting for jobs...")

    while not event.is_set():
        try:
            job = await db.get_pending_job()
            if not job:
                try:
                    await asyncio.wait_for(event.wait(), timeout=poll_interval)
                except asyncio.TimeoutError:
                    continue
                continue

            last_job_id = job['id']
            await process_job(db, job)
            processed_jobs += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception('Worker loop error: %s', exc)
            await asyncio.sleep(poll_interval)


async def process_job(db: Database, job: Dict[str, Any]):
    job_id = job['id']
    user_id = job['user_id']
    prompt_handler = PromptHandler()

    try:
        # Update status to processing
        await db.update_job(
            job_id,
            status='processing',
            latest_message='Starting content generation...',
        )

        # Fetch user's Gemini API key
        api_key = await db.get_user_api_key(user_id)

        if not api_key:
            raise RuntimeError('User API key not found')

        # Fetch user's custom prompts (or use defaults)
        user_prompts = await db.get_user_prompts(user_id)
        prompts = user_prompts if user_prompts else PROMPT_TEMPLATES

        logger.info(f"📝 Using {'custom' if user_prompts else 'default'} prompts")

        # Initialize Gemini generator
        generator = GeminiGenerator(api_key)

        # Fetch topics for this job
        topics = await db.get_job_topics(job_id)

        if not topics:
            raise RuntimeError('No topics associated with this job')

        logger.info(f"📝 Generating {len(topics)} pieces of content")

        # Track successful generations
        successful = 0
        failed = 0
        total_topics = len(topics)

        # Generate content for each topic
        for idx, topic_row in enumerate(topics, start=1):
            row_number = topic_row['row_number']
            topic = topic_row['topic']
            content_type = topic_row['content_type']

            # Get appropriate prompt template
            template_key = get_content_type_key(content_type)
            prompt_template = prompts.get(template_key, PROMPT_TEMPLATES.get(template_key, ''))

            # If still no template, use the exact content type as key
            if not prompt_template and content_type in prompts:
                prompt_template = prompts[content_type]

            # Fallback to default
            if not prompt_template:
                prompt_template = PROMPT_TEMPLATES.get('mixed', 'Create content about: {topic}')

            # Prepare the prompt with topic injection
            prompt = prompt_handler.prepare_prompt(prompt_template, topic, content_type)

            # Validate prompt length
            if not prompt_handler.validate_prompt_length(prompt):
                logger.warning(f"⚠️ Prompt too long for topic '{topic}' (length: {len(prompt)})")
                prompt = prompt[:90000] + f"\n\n[Truncated]\n\nTopic: {topic}"

            # Log prompt info for debugging
            requirements = prompt_handler.extract_requirements(prompt)
            logger.debug(f"Prompt stats: {requirements}")

            # Generate content
            try:
                generated_text = await generator.generate(prompt)

                # Clean up the generated content
                generated_text = prompt_handler.clean_generated_content(generated_text)

                # Update database
                await db.update_generated_content(
                    job_id=job_id,
                    row_number=row_number,
                    generated_text=generated_text,
                )

                successful += 1

                # Update progress
                await db.update_job(
                    job_id,
                    progress=idx,
                    latest_message=f"Generated {content_type} for: {topic[:50]}...",
                )

                logger.info(f"✅ [{idx}/{total_topics}] Generated: {topic[:40]}...")

            except Exception as exc:  # pylint: disable=broad-except
                logger.error(f"❌ Failed to generate for topic '{topic}': {exc}")
                failed += 1
                # Continue to next topic instead of failing entire job
                await db.update_job(
                    job_id,
                    progress=idx,
                    latest_message=f"Skipped row {row_number}: {str(exc)[:50]}...",
                )
                continue

        # Mark job as completed
        final_message = f'Successfully generated {successful}/{total_topics} pieces of content!'
        if failed > 0:
            final_message += f' ({failed} failed)'

        await db.update_job(
            job_id,
            status='completed',
            latest_message=final_message,
            completed_at=datetime.utcnow(),
        )

        # Update generation log
        await db.update_generation_log(user_id, job_id, successful)

        logger.info(f"🎉 Job {job_id} completed: {successful} successful, {failed} failed")

    except Exception as exc:  # pylint: disable=broad-except
        logger.exception('Job %s failed', job_id)
        await db.update_job(
            job_id,
            status='failed',
            error_message=str(exc),
            latest_message='Worker encountered an error',
        )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=int(os.getenv('PORT', '8000')))
