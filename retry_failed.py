"""
Retry script for failed topics (text-only workflow).
"""
import sys

from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from utils import logger, save_to_json, format_timestamp
from prompts import (
    get_thread_prompt,
    get_carousel_prompt,
    get_linkedin_prompt,
    get_short_post_prompt,
)


def retry_failed():
    """Retry all failed topics from the Failed sheet."""
    print("\n" + "=" * 60)
    print("🔄 RETRYING FAILED TOPICS")
    print("=" * 60 + "\n")

    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
    except Exception as e:
        logger.error(f"Retry initialization error: {e}", exc_info=True)
        print(f"❌ Initialization error: {e}")
        sys.exit(1)

    failed_topics = sheets.get_failed_topics(status="Pending Retry")
    if not failed_topics:
        print("✅ No failed topics to retry!")
        return

    print(f"Found {len(failed_topics)} failed topics\n")
    timestamp = format_timestamp()
    retried_content = []

    for failed in failed_topics:
        topic = failed.get("Topic", "")
        content_type = failed.get("Content Type", "")
        if not topic or not content_type:
            continue

        print(f"🔄 Retrying: {topic} ({content_type})")
        logger.info(f"[RETRY] Attempting {content_type} for topic: {topic}")

        try:
            if "Thread" in content_type:
                gemini._rate_limit_wait()
                response = gemini.model.generate_content(get_thread_prompt(topic))
                thread_text = response.text.strip()
                content = {
                    "topic": topic,
                    "x_thread": thread_text,
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "X Thread",
                }

            elif "Carousel" in content_type:
                gemini._rate_limit_wait()
                linkedin = gemini.model.generate_content(
                    get_carousel_prompt(topic, "linkedin")
                ).text.strip()

                gemini._rate_limit_wait()
                instagram = gemini.model.generate_content(
                    get_carousel_prompt(topic, "instagram")
                ).text.strip()

                content = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "linkedin_carousel": linkedin,
                    "instagram_carousel": instagram,
                    "content_type": "Carousel",
                }

            elif "LinkedIn" in content_type:
                gemini._rate_limit_wait()
                response = gemini.model.generate_content(get_linkedin_prompt(topic))
                post_text = response.text.strip()
                content = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": post_text,
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "LinkedIn Post",
                }

            elif "X Post" in content_type:
                gemini._rate_limit_wait()
                response = gemini.model.generate_content(
                    get_short_post_prompt(topic, "x")
                )
                post_text = response.text.strip()
                content = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": post_text,
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "X Post",
                }

            elif "Instagram" in content_type and "Short Post" not in content_type:
                gemini._rate_limit_wait()
                response = gemini.model.generate_content(
                    get_short_post_prompt(topic, "instagram")
                )
                caption_text = response.text.strip()
                content = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": caption_text,
                    "carousel_outline": "",
                    "content_type": "Instagram Caption",
                }

            elif "Short Post" in content_type:
                gemini._rate_limit_wait()
                x_response = gemini.model.generate_content(
                    get_short_post_prompt(topic, "x")
                )
                x_text = x_response.text.strip()

                gemini._rate_limit_wait()
                ig_response = gemini.model.generate_content(
                    get_short_post_prompt(topic, "instagram")
                )
                ig_text = ig_response.text.strip()

                content = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": x_text,
                    "linkedin_post": "",
                    "instagram_caption": ig_text,
                    "carousel_outline": "",
                    "content_type": "Short Post",
                }

            elif "Mixed" in content_type:
                mixed_result = gemini.generate_all([topic], batch_size=1)
                if not mixed_result:
                    raise Exception("Mixed content generation failed")
                entry = mixed_result[0]
                content = {
                    "topic": entry.get("topic", topic),
                    "x_thread": entry.get("x_thread", ""),
                    "x_post": entry.get("x_post", ""),
                    "linkedin_post": entry.get("linkedin_post", ""),
                    "instagram_caption": entry.get("instagram_caption", ""),
                    "carousel_outline": entry.get("carousel_outline", ""),
                    "content_type": "Mixed Content",
                }

            else:
                logger.warning(f"[RETRY] Unknown content type '{content_type}'")
                continue

            sheets.write_single_content(content)
            retried_content.append(content)
            sheets.mark_retry_complete(topic, content_type)
            print(f"✅ Success: {topic}")
            logger.info(f"[RETRY] Successfully retried {content_type} for topic: {topic}")

        except Exception as e:
            logger.error(f"[RETRY] Still failed for '{topic}': {e}", exc_info=True)
            print(f"❌ Still failed: {topic} → {e}")

    if retried_content:
        save_to_json(retried_content, f"retried_{timestamp}.json")
        for item in retried_content:
            if item.get("topic"):
                sheets.update_topic_status(item["topic"], "Generated")

    print(
        f"\n✅ Retry complete. Successfully retried: {len(retried_content)}/{len(failed_topics)}"
    )


if __name__ == "__main__":
    retry_failed()

