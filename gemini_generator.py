"""
Gemini API handler for content generation.
"""
import google.generativeai as genai
import json
import time
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_RPM, BATCH_SIZE
from utils import logger

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


class GeminiGenerator:
    def __init__(self):
        """Initialize Gemini model."""
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.request_count = 0
        self.last_request_time = time.time()
        logger.info(f"✅ Gemini {GEMINI_MODEL} initialized")
        print(f"✅ Gemini {GEMINI_MODEL} initialized")
    
    def _rate_limit_wait(self):
        """Enforce rate limiting (15 RPM for Gemini 2.5 Flash-Lite)."""
        elapsed = time.time() - self.last_request_time
        wait_time = 60 / GEMINI_RPM  # 4 seconds between requests for 15 RPM
        
        if elapsed < wait_time:
            sleep_duration = wait_time - elapsed
            logger.info(f"⏳ Rate limit: waiting {sleep_duration:.1f}s...")
            print(f"⏳ Rate limit: waiting {sleep_duration:.1f}s...")
            time.sleep(sleep_duration)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def _cooldown_wait(self):
        """1 minute cooldown between successful generations."""
        logger.info("😴 Cooldown: waiting 60s before next generation...")
        print("😴 Cooldown: waiting 60s before next generation...")
        time.sleep(60)
    
    def generate_content_batch(self, topics):
        """
        Generate ALL content types for a batch of topics.
        
        Args:
            topics: List of topic strings (max 5)
        
        Returns:
            List of generated content dictionaries
        """
        self._rate_limit_wait()
        
        topics_str = ", ".join(topics)
        
        prompt = f"""Generate social media content for these {len(topics)} topics.

Topics: {topics_str}

For EACH topic, create ALL of the following:

1. **X Post** (280 chars max, Aniket style: spicy + emoji + question)

2. **X Thread** (8-10 tweets, narrative-driven, educational, opinionated)

3. **LinkedIn Post** (4-6 paragraphs, thought leadership, storytelling)

4. **Instagram Caption** (casual, emojis, engagement question, hashtags)

5. **Carousel Outline** (6-8 slides with titles + talking points)

Return ONLY valid JSON in this exact format:

{{
  "content": [
    {{
      "topic": "topic1",
      "x_post": "...",
      "x_thread": "1. ...\\n2. ...\\n...",
      "linkedin_post": "...",
      "instagram_caption": "...",
      "carousel_outline": "Slide 1: ... | ...\\nSlide 2: ... | ...\\n..."
    }}
  ]
}}

NO MARKDOWN, NO EXPLANATIONS, ONLY THE JSON."""

        try:
            logger.info(f"[GEMINI] Generating batch for {len(topics)} topics")
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "")
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "")
            
            # Parse JSON
            data = json.loads(response_text)
            content_list = data.get("content", [])
            
            logger.info(f"[GEMINI] ✅ Generated content for {len(content_list)} topics")
            print(f"✅ Generated content for {len(content_list)} topics")
            
            # 1 MINUTE COOLDOWN AFTER SUCCESS
            self._cooldown_wait()
            
            return content_list
            
        except json.JSONDecodeError as e:
            logger.error(f"[GEMINI] JSON parse error: {e}")
            logger.error(f"Response preview: {response_text[:500]}...")
            print(f"❌ JSON parse error: {e}")
            return []
        except Exception as e:
            logger.error(f"[GEMINI] API error: {e}", exc_info=True)
            print(f"❌ Gemini API error: {e}")
            return []
    
    def generate_all(self, topics_list, batch_size=BATCH_SIZE):
        """
        Generate content for all topics in batches.
        
        Args:
            topics_list: List of all topics
            batch_size: Topics per batch (default: 5)
        
        Returns:
            List of all generated content
        """
        all_content = []
        total_batches = (len(topics_list) + batch_size - 1) // batch_size
        
        logger.info(f"[GEMINI] Starting generation for {len(topics_list)} topics in {total_batches} batches")
        print(f"\n📝 Generating content for {len(topics_list)} topics in {total_batches} batches...")
        
        for i in range(0, len(topics_list), batch_size):
            batch = topics_list[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            print(f"\n🔄 Batch {batch_num}/{total_batches}: {len(batch)} topics")
            logger.info(f"[GEMINI BATCH] Starting batch {batch_num}/{total_batches}")
            
            try:
                content = self.generate_content_batch(batch)
                all_content.extend(content)
                logger.info(f"[GEMINI BATCH] ✅ Batch {batch_num} complete. Total: {len(all_content)}")
                print(f"✅ Batch {batch_num} complete. Total generated: {len(all_content)}")
            except Exception as e:
                logger.error(f"[GEMINI BATCH] ❌ Batch {batch_num} failed: {e}", exc_info=True)
                print(f"❌ Batch {batch_num} failed → {e}")
                continue
        
        logger.info(f"[GEMINI] Generation complete. Total: {len(all_content)} pieces")
        return all_content
