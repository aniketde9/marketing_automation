"""
Main automation script with row-based content distribution (text only).
"""
import sys
from collections import Counter

from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from prompts import (
    get_carousel_prompt,
    get_thread_prompt,
    get_linkedin_prompt,
    get_short_post_prompt,
)
from utils import (
    save_to_json,
    format_timestamp,
    logger,
    log_failure,
    get_failure_summary,
    clear_failures,
)

# Distribution map (rows are inclusive, sheet rows start at 2)
DISTRIBUTION = {
    "carousels_batch1": (2, 31),       # 30 carousels (replaces videos)
    "x_threads": (32, 51),             # 20 X threads
    "carousels_batch2": (52, 71),      # 20 carousels
    "linkedin_posts": (72, 91),        # 20 LinkedIn posts
    "x_posts": (92, 111),              # 20 X posts
    "instagram_captions": (112, 151),  # 40 IG captions
    "mixed_all": (152, 161),           # 10 topics, all formats
    "short_posts": (162, 201),         # 40 short posts (X + IG)
}


def get_topics_by_range(topics_data, start_row, end_row):
    start_idx = start_row - 2  # Row 2 -> index 0
    end_idx = end_row - 2 + 1
    return [
        row["Topic"]
        for row in topics_data[start_idx:end_idx]
        if row.get("Topic")
    ]


def main():
    print("\n" + "=" * 60)
    print("🚀 MARKETING AUTOMATION BOT (TEXT ONLY)")
    print("=" * 60 + "\n")

    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
    except Exception as e:
        logger.error(f"Initialization error: {e}", exc_info=True)
        print(f"❌ Initialization error: {e}")
        sys.exit(1)

    print("📋 Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=200, status="Pending")

    if len(topics_data) < 200:
        logger.warning(f"Only {len(topics_data)} topics found. Expected 200.")
        print(f"⚠️ Warning: Only {len(topics_data)} topics found. Expected 200.")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != "y":
            sys.exit(0)

    print(f"✅ Loaded {len(topics_data)} topics\n")
    clear_failures()
    timestamp = format_timestamp()

    carousel_content_1 = []
    thread_content = []
    carousel_content_2 = []
    linkedin_content = []
    x_post_content = []
    ig_content = []
    mixed_content = []
    short_content = []

    # ------------------------------------------------------------
    # Step 1: Carousels (Rows 2-31)
    # ------------------------------------------------------------
    carousel_topics_1 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch1"]
    )
    print(f"🎨 Step 1: Generating {len(carousel_topics_1)} carousels (Rows 2-31)...")

    for topic in carousel_topics_1:
        logger.info(f"[CAROUSEL B1] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }
            sheets.write_single_content(content_dict)
            carousel_content_1.append(content_dict)
        except Exception as e:
            logger.error(f"[CAROUSEL B1] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_1:
        save_to_json(carousel_content_1, f"carousels_batch1_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 2: X Threads (Rows 32-51)
    # ------------------------------------------------------------
    thread_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_threads"])
    print(f"\n🧵 Step 2: Generating {len(thread_topics)} X threads (Rows 32-51)...")

    for topic in thread_topics:
        logger.info(f"[THREAD] Generating for '{topic}'")
        try:
            prompt = get_thread_prompt(topic)
            gemini._rate_limit_wait()
            response = gemini.model.generate_content(prompt)
            thread_text = response.text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": thread_text,
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Thread",
            }
            sheets.write_single_content(content_dict)
            thread_content.append(content_dict)
        except Exception as e:
            logger.error(f"[THREAD] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ THREAD failed for '{topic}': {e}")
            log_failure(topic, "X Thread", str(e))
            sheets.write_failed_topic(topic, "X Thread", str(e))

    if thread_content:
        save_to_json(thread_content, f"x_threads_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 3: Carousels (Rows 52-71)
    # ------------------------------------------------------------
    carousel_topics_2 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch2"]
    )
    print(f"\n🎨 Step 3: Generating {len(carousel_topics_2)} carousels (Rows 52-71)...")

    for topic in carousel_topics_2:
        logger.info(f"[CAROUSEL B2] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }
            sheets.write_single_content(content_dict)
            carousel_content_2.append(content_dict)
        except Exception as e:
            logger.error(f"[CAROUSEL B2] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_2:
        save_to_json(carousel_content_2, f"carousels_batch2_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 4: LinkedIn Posts (Rows 72-91)
    # ------------------------------------------------------------
    linkedin_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["linkedin_posts"]
    )
    print(f"\n💼 Step 4: Generating {len(linkedin_topics)} LinkedIn posts (Rows 72-91)...")

    for topic in linkedin_topics:
        logger.info(f"[LINKEDIN] Generating for '{topic}'")
        try:
            prompt = get_linkedin_prompt(topic)
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": post_text,
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "LinkedIn Post",
            }
            sheets.write_single_content(content_dict)
            linkedin_content.append(content_dict)
        except Exception as e:
            logger.error(f"[LINKEDIN] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ LINKEDIN POST failed for '{topic}': {e}")
            log_failure(topic, "LinkedIn Post", str(e))
            sheets.write_failed_topic(topic, "LinkedIn Post", str(e))

    if linkedin_content:
        save_to_json(linkedin_content, f"linkedin_posts_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 5: X Posts (Rows 92-111)
    # ------------------------------------------------------------
    x_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_posts"])
    print(f"\n🐦 Step 5: Generating {len(x_topics)} X posts (Rows 92-111)...")

    for topic in x_topics:
        logger.info(f"[X POST] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": post_text,
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Post",
            }
            sheets.write_single_content(content_dict)
            x_post_content.append(content_dict)
        except Exception as e:
            logger.error(f"[X POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ X POST failed for '{topic}': {e}")
            log_failure(topic, "X Post", str(e))
            sheets.write_failed_topic(topic, "X Post", str(e))

    if x_post_content:
        save_to_json(x_post_content, f"x_posts_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 6: Instagram Captions (Rows 112-151)
    # ------------------------------------------------------------
    ig_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["instagram_captions"]
    )
    print(f"\n📸 Step 6: Generating {len(ig_topics)} Instagram captions (Rows 112-151)...")

    for topic in ig_topics:
        logger.info(f"[INSTAGRAM] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            caption_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": caption_text,
                "carousel_outline": "",
                "content_type": "Instagram Caption",
            }
            sheets.write_single_content(content_dict)
            ig_content.append(content_dict)
        except Exception as e:
            logger.error(f"[INSTAGRAM] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ INSTAGRAM CAPTION failed for '{topic}': {e}")
            log_failure(topic, "Instagram Caption", str(e))
            sheets.write_failed_topic(topic, "Instagram Caption", str(e))

    if ig_content:
        save_to_json(ig_content, f"instagram_captions_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 7: Mixed Formats (Rows 152-161)
    # ------------------------------------------------------------
    mixed_topics = get_topics_by_range(topics_data, *DISTRIBUTION["mixed_all"])
    print(f"\n🎯 Step 7: Generating ALL formats for {len(mixed_topics)} topics (Rows 152-161)...")

    if mixed_topics:
        logger.info(f"[MIXED] Generating all formats for {len(mixed_topics)} topics")
        try:
            batch_content = gemini.generate_all(mixed_topics, batch_size=5)
            for entry in batch_content:
                content_dict = {
                    "topic": entry.get("topic", ""),
                    "x_thread": entry.get("x_thread", ""),
                    "x_post": entry.get("x_post", ""),
                    "linkedin_post": entry.get("linkedin_post", ""),
                    "instagram_caption": entry.get("instagram_caption", ""),
                    "carousel_outline": entry.get("carousel_outline", ""),
                    "content_type": "Mixed Content",
                }
                sheets.write_single_content(content_dict)
                mixed_content.append(content_dict)
        except Exception as e:
            logger.error(f"[MIXED] Batch generation failed: {e}", exc_info=True)
            print(f"❌ MIXED batch failed: {e}")
            for topic in mixed_topics:
                log_failure(topic, "Mixed Content", str(e))
                sheets.write_failed_topic(topic, "Mixed Content", str(e))

    if mixed_content:
        save_to_json(mixed_content, f"mixed_content_{timestamp}.json")

    # ------------------------------------------------------------
    # Step 8: Short Posts (Rows 162-201)
    # ------------------------------------------------------------
    short_topics = get_topics_by_range(topics_data, *DISTRIBUTION["short_posts"])
    print(f"\n⚡ Step 8: Generating {len(short_topics)} short posts (Rows 162-201)...")

    for topic in short_topics:
        logger.info(f"[SHORT POST] Generating for '{topic}'")
        try:
            x_prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            x_post_text = gemini.model.generate_content(x_prompt).text.strip()

            ig_prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            ig_caption_text = gemini.model.generate_content(ig_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": x_post_text,
                "linkedin_post": "",
                "instagram_caption": ig_caption_text,
                "carousel_outline": "",
                "content_type": "Short Post",
            }
            sheets.write_single_content(content_dict)
            short_content.append(content_dict)
        except Exception as e:
            logger.error(f"고
"""
Main automation script with row-based content distribution (text-only).
"""
import sys
from collections import Counter

from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from prompts import (
    get_carousel_prompt,
    get_thread_prompt,
    get_linkedin_prompt,
    get_short_post_prompt,
)
from utils import (
    save_to_json,
    format_timestamp,
    logger,
    log_failure,
    get_failure_summary,
    clear_failures,
)

DISTRIBUTION = {
    "carousels_batch1": (2, 31),
    "x_threads": (32, 51),
    "carousels_batch2": (52, 71),
    "linkedin_posts": (72, 91),
    "x_posts": (92, 111),
    "instagram_captions": (112, 151),
    "mixed_all": (152, 161),
    "short_posts": (162, 201),
}


def get_topics_by_range(topics_data, start_row, end_row):
    start_idx = start_row - 2
    end_idx = end_row - 2 + 1
    return [
        row["Topic"]
        for row in topics_data[start_idx:end_idx]
        if row.get("Topic")
    ]


def main():
    print("\n" + "=" * 60)
    print("🚀 MARKETING AUTOMATION BOT (TEXT ONLY)")
    print("=" * 60 + "\n")

    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
    except Exception as e:
        logger.error(f"Initialization error: {e}", exc_info=True)
        print(f"❌ Initialization error: {e}")
        sys.exit(1)

    print("📋 Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=200, status="Pending")

    if len(topics_data) < 200:
        logger.warning(f"Only {len(topics_data)} topics found. Expected 200.")
        print(f"⚠️ Warning: Only {len(topics_data)} topics found. Expected 200.")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != "y":
            sys.exit(0)

    print(f"✅ Loaded {len(topics_data)} topics\n")
    clear_failures()
    timestamp = format_timestamp()

    carousel_content_1 = []
    thread_content = []
    carousel_content_2 = []
    linkedin_content = []
    x_post_content = []
    ig_content = []
    mixed_content = []
    short_content = []

    # STEP 1: CAROUSELS (Rows 2-31)
    carousel_topics_1 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch1"]
    )
    print(f"🎨 Step 1: Generating {len(carousel_topics_1)} carousels (Rows 2-31)...")
    for topic in carousel_topics_1:
        logger.info(f"[CAROUSEL B1] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }
            sheets.write_single_content(content_dict)
            carousel_content_1.append(content_dict)
        except Exception as e:
            logger.error(f"[CAROUSEL B1] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_1:
        save_to_json(carousel_content_1, f"carousels_batch1_{timestamp}.json")

    # STEP 2: X THREADS (Rows 32-51)
    thread_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_threads"])
    print(f"\n🧵 Step 2: Generating {len(thread_topics)} X threads (Rows 32-51)...")
    for topic in thread_topics:
        logger.info(f"[THREAD] Generating for '{topic}'")
        try:
            prompt = get_thread_prompt(topic)
            gemini._rate_limit_wait()
            response = gemini.model.generate_content(prompt)
            thread_text = response.text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": thread_text,
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Thread",
            }
            sheets.write_single_content(content_dict)
            thread_content.append(content_dict)
        except Exception as e:
            logger.error(f"[THREAD] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ THREAD failed for '{topic}': {e}")
            log_failure(topic, "X Thread", str(e))
            sheets.write_failed_topic(topic, "X Thread", str(e))

    if thread_content:
        save_to_json(thread_content, f"x_threads_{timestamp}.json")

    # STEP 3: CAROUSELS (Rows 52-71)
    carousel_topics_2 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch2"]
    )
    print(f"\n🎨 Step 3: Generating {len(carousel_topics_2)} carousels (Rows 52-71)...")
    for topic in carousel_topics_2:
        logger.info(f"[CAROUSEL B2] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }
            sheets.write_single_content(content_dict)
            carousel_content_2.append(content_dict)
        except Exception as e:
            logger.error(f"[CAROUSEL B2] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_2:
        save_to_json(carousel_content_2, f"carousels_batch2_{timestamp}.json")

    # STEP 4: LINKEDIN POSTS (Rows 72-91)
    linkedin_topics = get_topics_by_range(topics_data, *DISTRIBUTION["linkedin_posts"])
    print(f"\n💼 Step 4: Generating {len(linkedin_topics)} LinkedIn posts (Rows 72-91)...")
    for topic in linkedin_topics:
        logger.info(f"[LINKEDIN] Generating for '{topic}'")
        try:
            prompt = get_linkedin_prompt(topic)
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": post_text,
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "LinkedIn Post",
            }
            sheets.write_single_content(content_dict)
            linkedin_content.append(content_dict)
        except Exception as e:
            logger.error(f"[LINKEDIN] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ LINKEDIN POST failed for '{topic}': {e}")
            log_failure(topic, "LinkedIn Post", str(e))
            sheets.write_failed_topic(topic, "LinkedIn Post", str(e))

    if linkedin_content:
        save_to_json(linkedin_content, f"linkedin_posts_{timestamp}.json")

    # STEP 5: X POSTS (Rows 92-111)
    x_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_posts"])
    print(f"\n🐦 Step 5: Generating {len(x_topics)} X posts (Rows 92-111)...")
    for topic in x_topics:
        logger.info(f"[X POST] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": post_text,
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Post",
            }
            sheets.write_single_content(content_dict)
            x_post_content.append(content_dict)
        except Exception as e:
            logger.error(f"[X POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ X POST failed for '{topic}': {e}")
            log_failure(topic, "X Post", str(e))
            sheets.write_failed_topic(topic, "X Post", str(e))

    if x_post_content:
        save_to_json(x_post_content, f"x_posts_{timestamp}.json")

    # STEP 6: INSTAGRAM CAPTIONS (Rows 112-151)
    ig_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["instagram_captions"]
    )
    print(f"\n📸 Step 6: Generating {len(ig_topics)} Instagram captions (Rows 112-151)...")
    for topic in ig_topics:
        logger.info(f"[INSTAGRAM] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            caption_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": caption_text,
                "carousel_outline": "",
                "content_type": "Instagram Caption",
            }
            sheets.write_single_content(content_dict)
            ig_content.append(content_dict)
        except Exception as e:
            logger.error(f"[INSTAGRAM] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ INSTAGRAM CAPTION failed for '{topic}': {e}")
            log_failure(topic, "Instagram Caption", str(e))
            sheets.write_failed_topic(topic, "Instagram Caption", str(e))

    if ig_content:
        save_to_json(ig_content, f"instagram_captions_{timestamp}.json")

    # STEP 7: MIXED (Rows 152-161)
    mixed_topics = get_topics_by_range(topics_data, *DISTRIBUTION["mixed_all"])
    print(f"\n🎯 Step 7: Generating ALL formats for {len(mixed_topics)} topics (Rows 152-161)...")
    if mixed_topics:
        logger.info(f"[MIXED] Generating all formats for {len(mixed_topics)} topics")
        try:
            batch_content = gemini.generate_all(mixed_topics, batch_size=5)
            for entry in batch_content:
                content_dict = {
                    "topic": entry.get("topic", ""),
                    "x_thread": entry.get("x_thread", ""),
                    "x_post": entry.get("x_post", ""),
                    "linkedin_post": entry.get("linkedin_post", ""),
                    "instagram_caption": entry.get("instagram_caption", ""),
                    "carousel_outline": entry.get("carousel_outline", ""),
                    "content_type": "Mixed Content",
                }
                sheets.write_single_content(content_dict)
                mixed_content.append(content_dict)
        except Exception as e:
            logger.error(f"[MIXED] Batch generation failed: {e}", exc_info=True)
            print(f"❌ MIXED batch failed: {e}")
            for topic in mixed_topics:
                log_failure(topic, "Mixed Content", str(e))
                sheets.write_failed_topic(topic, "Mixed Content", str(e))

    if mixed_content:
        save_to_json(mixed_content, f"mixed_content_{timestamp}.json")

    # STEP 8: SHORT POSTS (Rows 162-201)
    short_topics = get_topics_by_range(topics_data, *DISTRIBUTION["short_posts"])
    print(f"\n⚡ Step 8: Generating {len(short_topics)} short posts (Rows 162-201)...")
    for topic in short_topics:
        logger.info(f"[SHORT POST] Generating for '{topic}'")
        try:
            x_prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            x_post_text = gemini.model.generate_content(x_prompt).text.strip()

            ig_prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            ig_caption_text = gemini.model.generate_content(ig_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": x_post_text,
                "linkedin_post": "",
                "instagram_caption": ig_caption_text,
                "carousel_outline": "",
                "content_type": "Short Post",
            }
            sheets.write_single_content(content_dict)
            short_content.append(content_dict)
        except Exception as e:
            logger.error(f"고
"""
Main automation script with row-based content distribution (text-only).
"""
import sys
from collections import Counter

from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from utils import (
    save_to_json,
    format_timestamp,
    logger,
    log_failure,
    get_failure_summary,
    clear_failures,
)
from prompts import (
    get_carousel_prompt,
    get_thread_prompt,
    get_linkedin_prompt,
    get_short_post_prompt,
)

DISTRIBUTION = {
    "carousels_batch1": (2, 31),
    "x_threads": (32, 51),
    "carousels_batch2": (52, 71),
    "linkedin_posts": (72, 91),
    "x_posts": (92, 111),
    "instagram_captions": (112, 151),
    "mixed_all": (152, 161),
    "short_posts": (162, 201),
}


def get_topics_by_range(topics_data, start_row, end_row):
    start_idx = start_row - 2
    end_idx = end_row - 2 + 1
    return [
        row["Topic"]
        for row in topics_data[start_idx:end_idx]
        if row.get("Topic")
    ]


def main():
    print("\n" + "=" * 60)
    print("🚀 MARKETING AUTOMATION BOT (TEXT ONLY)")
    print("=" * 60 + "\n")

    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
    except Exception as e:
        logger.error(f"Initialization error: {e}", exc_info=True)
        print(f"❌ Initialization error: {e}")
        sys.exit(1)

    print("📋 Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=200, status="Pending")

    if len(topics_data) < 200:
        logger.warning(f"Only {len(topics_data)} topics found. Expected 200.")
        print(f"⚠️ Warning: Only {len(topics_data)} topics found. Expected 200.")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != "y":
            sys.exit(0)

    print(f"✅ Loaded {len(topics_data)} topics\n")
    clear_failures()
    timestamp = format_timestamp()

    carousel_content_1 = []
    thread_content = []
    carousel_content_2 = []
    linkedin_content = []
    x_post_content = []
    ig_content = []
    mixed_content = []
    short_content = []

    carousel_topics_1 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch1"]
    )
    print(f"🎨 Step 1: Generating {len(carousel_topics_1)} carousels (Rows 2-31)...")

    for topic in carousel_topics_1:
        logger.info(f"[CAROUSEL B1] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }

            sheets.write_single_content(content_dict)
            carousel_content_1.append(content_dict)
            logger.info(f"[CAROUSEL B1] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[CAROUSEL B1] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_1:
        save_to_json(carousel_content_1, f"carousels_batch1_{timestamp}.json")

    thread_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_threads"])
    print(f"\n🧵 Step 2: Generating {len(thread_topics)} X threads (Rows 32-51)...")

    for topic in thread_topics:
        logger.info(f"[THREAD] Generating for '{topic}'")
        try:
            prompt = get_thread_prompt(topic)
            gemini._rate_limit_wait()
            response = gemini.model.generate_content(prompt)
            thread_text = response.text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": thread_text,
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Thread",
            }

            sheets.write_single_content(content_dict)
            thread_content.append(content_dict)
            logger.info(f"[THREAD] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[THREAD] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ THREAD failed for '{topic}': {e}")
            log_failure(topic, "X Thread", str(e))
            sheets.write_failed_topic(topic, "X Thread", str(e))

    if thread_content:
        save_to_json(thread_content, f"x_threads_{timestamp}.json")

    carousel_topics_2 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch2"]
    )
    print(f"\n🎨 Step 3: Generating {len(carousel_topics_2)} carousels (Rows 52-71)...")

    for topic in carousel_topics_2:
        logger.info(f"[CAROUSEL B2] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }

            sheets.write_single_content(content_dict)
            carousel_content_2.append(content_dict)
            logger.info(f"[CAROUSEL B2] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[CAROUSEL B2] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_2:
        save_to_json(carousel_content_2, f"carousels_batch2_{timestamp}.json")

    linkedin_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["linkedin_posts"]
    )
    print(f"\n💼 Step 4: Generating {len(linkedin_topics)} LinkedIn posts (Rows 72-91)...")

    for topic in linkedin_topics:
        logger.info(f"[LINKEDIN] Generating for '{topic}'")
        try:
            prompt = get_linkedin_prompt(topic)
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": post_text,
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "LinkedIn Post",
            }

            sheets.write_single_content(content_dict)
            linkedin_content.append(content_dict)
            logger.info(f"[LINKEDIN] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[LINKEDIN] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ LINKEDIN POST failed for '{topic}': {e}")
            log_failure(topic, "LinkedIn Post", str(e))
            sheets.write_failed_topic(topic, "LinkedIn Post", str(e))

    if linkedin_content:
        save_to_json(linkedin_content, f"linkedin_posts_{timestamp}.json")

    x_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_posts"])
    print(f"\n🐦 Step 5: Generating {len(x_topics)} X posts (Rows 92-111)...")

    for topic in x_topics:
        logger.info(f"[X POST] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": post_text,
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Post",
            }

            sheets.write_single_content(content_dict)
            x_post_content.append(content_dict)
            logger.info(f"[X POST] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[X POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ X POST failed for '{topic}': {e}")
            log_failure(topic, "X Post", str(e))
            sheets.write_failed_topic(topic, "X Post", str(e))

    if x_post_content:
        save_to_json(x_post_content, f"x_posts_{timestamp}.json")

    ig_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["instagram_captions"]
    )
    print(f"\n📸 Step 6: Generating {len(ig_topics)} Instagram captions (Rows 112-151)...")

    for topic in ig_topics:
        logger.info(f"[INSTAGRAM] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            caption_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": caption_text,
                "carousel_outline": "",
                "content_type": "Instagram Caption",
            }

            sheets.write_single_content(content_dict)
            ig_content.append(content_dict)
            logger.info(f"[INSTAGRAM] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[INSTAGRAM] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ INSTAGRAM CAPTION failed for '{topic}': {e}")
            log_failure(topic, "Instagram Caption", str(e))
            sheets.write_failed_topic(topic, "Instagram Caption", str(e))

    if ig_content:
        save_to_json(ig_content, f"instagram_captions_{timestamp}.json")

    mixed_topics = get_topics_by_range(topics_data, *DISTRIBUTION["mixed_all"])
    print(f"\n🎯 Step 7: Generating ALL formats for {len(mixed_topics)} topics (Rows 152-161)...")

    if mixed_topics:
        logger.info(f"[MIXED] Generating all formats for {len(mixed_topics)} topics")
        try:
            batch_content = gemini.generate_all(mixed_topics, batch_size=5)
            for entry in batch_content:
                content_dict = {
                    "topic": entry.get("topic", ""),
                    "x_thread": entry.get("x_thread", ""),
                    "x_post": entry.get("x_post", ""),
                    "linkedin_post": entry.get("linkedin_post", ""),
                    "instagram_caption": entry.get("instagram_caption", ""),
                    "carousel_outline": entry.get("carousel_outline", ""),
                    "content_type": "Mixed Content",
                }
                sheets.write_single_content(content_dict)
                mixed_content.append(content_dict)
        except Exception as e:
            logger.error(f"[MIXED] Batch generation failed: {e}", exc_info=True)
            print(f"❌ MIXED batch failed: {e}")
            for topic in mixed_topics:
                log_failure(topic, "Mixed Content", str(e))
                sheets.write_failed_topic(topic, "Mixed Content", str(e))

    if mixed_content:
        save_to_json(mixed_content, f"mixed_content_{timestamp}.json")

    short_topics = get_topics_by_range(topics_data, *DISTRIBUTION["short_posts"])
    print(f"\n⚡ Step 8: Generating {len(short_topics)} short posts (Rows 162-201)...")

    for topic in short_topics:
        logger.info(f"[SHORT POST] Generating for '{topic}'")
        try:
            x_prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            x_post_text = gemini.model.generate_content(x_prompt).text.strip()

            ig_prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            ig_caption_text = gemini.model.generate_content(ig_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": x_post_text,
                "linkedin_post": "",
                "instagram_caption": ig_caption_text,
                "carousel_outline": "",
                "content_type": "Short Post",
            }

            sheets.write_single_content(content_dict)
            short_content.append(content_dict)
            logger.info(f"[SHORT POST] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[SHORT POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ SHORT POST failed for '{topic}': {e}")
            log_failure(topic, "Short Post", str(e))
            sheets.write_failed_topic(topic, "Short Post", str(e))

    if short_content:
        save_to_json(short_content, f"short_posts_{timestamp}.json")

    all_content = (
        carousel_content_1
        + thread_content
        + carousel_content_2
        + linkedin_content
        + x_post_content
        + ig_content
        + mixed_content
        + short_content
    )

    for item in all_content:
        if item.get("topic"):
            sheets.update_topic_status(item["topic"], "Generated")

    failures = get_failure_summary()
    total_carousels = len(carousel_content_1) + len(carousel_content_2)

    print("\n" + "=" * 60)
    print("📊 GENERATION COMPLETE")
    print("=" * 60)
    print(f"🎨 Carousels (Rows 2-31): {len(carousel_content_1)}")
    print(f"🧵 X Threads: {len(thread_content)}")
    print(f"🎨 Carousels (Rows 52-71): {len(carousel_content_2)}")
    print(f"💼 LinkedIn Posts: {len(linkedin_content)}")
    print(f"🐦 X Posts: {len(x_post_content)}")
    print(f"📸 Instagram Captions: {len(ig_content)}")
    print(f"🎯 Mixed Content (all formats): {len(mixed_content)}")
    print(f"⚡ Short Posts (X + IG): {len(short_content)}")
    print(f"\n📈 TOTAL CAROUSELS: {total_carousels}")
    print(f"📝 TOTAL TEXT PIECES: {len(all_content)}")

    if failures:
        print(f"\n⚠️ FAILURES: {len(failures)}")
        failure_counts = Counter(f["content_type"] for f in failures)
        for content_type, count in failure_counts.items():
            print(f"   - {content_type}: {count}")
        print("\n❌ Failed topics logged to 'Failed' sheet")
        print("📄 Check logs/run.log for detailed errors")
    else:
        print("\n🎉 NO FAILURES - All content generated successfully!")

    print("\n✅ All content saved to:")
    print("   - Google Sheets (Generated_Posts tab)")
    print("   - output/posts/*.json")
    print("   - logs/run.log")
    print("=" * 60)


if __name__ == "__main__":
    main()
"""
Main automation script with row-based content distribution (text-only).
"""
import sys
from collections import Counter

from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from utils import (
    save_to_json,
    format_timestamp,
    logger,
    log_failure,
    get_failure_summary,
    clear_failures,
)
from prompts import (
    get_carousel_prompt,
    get_thread_prompt,
    get_linkedin_prompt,
    get_short_post_prompt,
)

# ============================================================
# ROW-BASED DISTRIBUTION STRATEGY (NO VIDEO GENERATION)
# ============================================================
DISTRIBUTION = {
    "carousels_batch1": (2, 31),      # Rows 2-31: 30 carousels (was videos)
    "x_threads": (32, 51),            # Rows 32-51: 20 X threads
    "carousels_batch2": (52, 71),     # Rows 52-71: 20 more carousels
    "linkedin_posts": (72, 91),       # Rows 72-91: 20 LinkedIn posts
    "x_posts": (92, 111),             # Rows 92-111: 20 X posts
    "instagram_captions": (112, 151), # Rows 112-151: 40 Instagram captions
    "mixed_all": (152, 161),          # Rows 152-161: 10 topics, all formats
    "short_posts": (162, 201),        # Rows 162-201: 40 topics (X + IG)
}


def get_topics_by_range(topics_data, start_row, end_row):
    """
    Extract topics within a specific row range.

    Args:
        topics_data: List of all topic rows from sheet
        start_row: Starting row number (inclusive)
        end_row: Ending row number (inclusive)

    Returns:
        List of topics in that range
    """
    start_idx = start_row - 2  # Row 2 -> index 0
    end_idx = end_row - 2 + 1  # Inclusive
    return [
        row["Topic"]
        for row in topics_data[start_idx:end_idx]
        if row.get("Topic")
    ]


def main():
    print("\n" + "=" * 60)
    print("🚀 MARKETING AUTOMATION BOT (TEXT ONLY)")
    print("=" * 60 + "\n")

    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
    except Exception as e:
        logger.error(f"Initialization error: {e}", exc_info=True)
        print(f"❌ Initialization error: {e}")
        sys.exit(1)

    print("📋 Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=200, status="Pending")

    if len(topics_data) < 200:
        logger.warning(f"Only {len(topics_data)} topics found. Expected 200.")
        print(f"⚠️ Warning: Only {len(topics_data)} topics found. Expected 200.")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != "y":
            sys.exit(0)

    print(f"✅ Loaded {len(topics_data)} topics\n")
    clear_failures()
    timestamp = format_timestamp()

    # Storage for summaries/status updates
    carousel_content_1 = []
    thread_content = []
    carousel_content_2 = []
    linkedin_content = []
    x_post_content = []
    ig_content = []
    mixed_content = []
    short_content = []

    # ============================================================
    # STEP 1: CAROUSELS (Rows 2-31)
    # ============================================================
    carousel_topics_1 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch1"]
    )
    print(f"🎨 Step 1: Generating {len(carousel_topics_1)} carousels (Rows 2-31)...")

    for topic in carousel_topics_1:
        logger.info(f"[CAROUSEL B1] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }

            sheets.write_single_content(content_dict)
            carousel_content_1.append(content_dict)
            logger.info(f"[CAROUSEL B1] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[CAROUSEL B1] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_1:
        save_to_json(carousel_content_1, f"carousels_batch1_{timestamp}.json")

    # ============================================================
    # STEP 2: X THREADS (Rows 32-51)
    # ============================================================
    thread_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_threads"])
    print(f"\n🧵 Step 2: Generating {len(thread_topics)} X threads (Rows 32-51)...")

    for topic in thread_topics:
        logger.info(f"[THREAD] Generating for '{topic}'")
        try:
            prompt = get_thread_prompt(topic)
            gemini._rate_limit_wait()
            response = gemini.model.generate_content(prompt)
            thread_text = response.text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": thread_text,
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Thread",
            }

            sheets.write_single_content(content_dict)
            thread_content.append(content_dict)
            logger.info(f"[THREAD] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[THREAD] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ THREAD failed for '{topic}': {e}")
            log_failure(topic, "X Thread", str(e))
            sheets.write_failed_topic(topic, "X Thread", str(e))

    if thread_content:
        save_to_json(thread_content, f"x_threads_{timestamp}.json")

    # ============================================================
    # STEP 3: CAROUSELS (Rows 52-71)
    # ============================================================
    carousel_topics_2 = get_topics_by_range(
        topics_data, *DISTRIBUTION["carousels_batch2"]
    )
    print(f"\n🎨 Step 3: Generating {len(carousel_topics_2)} carousels (Rows 52-71)...")

    for topic in carousel_topics_2:
        logger.info(f"[CAROUSEL B2] Generating for '{topic}'")
        try:
            linkedin_prompt = get_carousel_prompt(topic, "linkedin")
            gemini._rate_limit_wait()
            linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()

            instagram_prompt = get_carousel_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "linkedin_carousel": linkedin_carousel,
                "instagram_carousel": instagram_carousel,
                "content_type": "Carousel",
            }

            sheets.write_single_content(content_dict)
            carousel_content_2.append(content_dict)
            logger.info(f"[CAROUSEL B2] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[CAROUSEL B2] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ CAROUSEL failed for '{topic}': {e}")
            log_failure(topic, "Carousel", str(e))
            sheets.write_failed_topic(topic, "Carousel", str(e))

    if carousel_content_2:
        save_to_json(carousel_content_2, f"carousels_batch2_{timestamp}.json")

    # ============================================================
    # STEP 4: LINKEDIN POSTS (Rows 72-91)
    # ============================================================
    linkedin_topics = get_topics_by_range(topics_data, *DISTRIBUTION["linkedin_posts"])
    print(f"\n💼 Step 4: Generating {len(linkedin_topics)} LinkedIn posts (Rows 72-91)...")

    for topic in linkedin_topics:
        logger.info(f"[LINKEDIN] Generating for '{topic}'")
        try:
            prompt = get_linkedin_prompt(topic)
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": post_text,
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "LinkedIn Post",
            }

            sheets.write_single_content(content_dict)
            linkedin_content.append(content_dict)
            logger.info(f"[LINKEDIN] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[LINKEDIN] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ LINKEDIN POST failed for '{topic}': {e}")
            log_failure(topic, "LinkedIn Post", str(e))
            sheets.write_failed_topic(topic, "LinkedIn Post", str(e))

    if linkedin_content:
        save_to_json(linkedin_content, f"linkedin_posts_{timestamp}.json")

    # ============================================================
    # STEP 5: X POSTS (Rows 92-111)
    # ============================================================
    x_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_posts"])
    print(f"\n🐦 Step 5: Generating {len(x_topics)} X posts (Rows 92-111)...")

    for topic in x_topics:
        logger.info(f"[X POST] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            post_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": post_text,
                "linkedin_post": "",
                "instagram_caption": "",
                "carousel_outline": "",
                "content_type": "X Post",
            }

            sheets.write_single_content(content_dict)
            x_post_content.append(content_dict)
            logger.info(f"[X POST] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[X POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ X POST failed for '{topic}': {e}")
            log_failure(topic, "X Post", str(e))
            sheets.write_failed_topic(topic, "X Post", str(e))

    if x_post_content:
        save_to_json(x_post_content, f"x_posts_{timestamp}.json")

    # ============================================================
    # STEP 6: INSTAGRAM CAPTIONS (Rows 112-151)
    # ============================================================
    ig_topics = get_topics_by_range(
        topics_data, *DISTRIBUTION["instagram_captions"]
    )
    print(f"\n📸 Step 6: Generating {len(ig_topics)} Instagram captions (Rows 112-151)...")

    for topic in ig_topics:
        logger.info(f"[INSTAGRAM] Generating for '{topic}'")
        try:
            prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            caption_text = gemini.model.generate_content(prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": "",
                "linkedin_post": "",
                "instagram_caption": caption_text,
                "carousel_outline": "",
                "content_type": "Instagram Caption",
            }

            sheets.write_single_content(content_dict)
            ig_content.append(content_dict)
            logger.info(f"[INSTAGRAM] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[INSTAGRAM] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ INSTAGRAM CAPTION failed for '{topic}': {e}")
            log_failure(topic, "Instagram Caption", str(e))
            sheets.write_failed_topic(topic, "Instagram Caption", str(e))

    if ig_content:
        save_to_json(ig_content, f"instagram_captions_{timestamp}.json")

    # ============================================================
    # STEP 7: MIXED FORMATS (Rows 152-161)
    # ============================================================
    mixed_topics = get_topics_by_range(topics_data, *DISTRIBUTION["mixed_all"])
    print(f"\n🎯 Step 7: Generating ALL formats for {len(mixed_topics)} topics (Rows 152-161)...")

    if mixed_topics:
        logger.info(f"[MIXED] Generating all formats for {len(mixed_topics)} topics")
        try:
            batch_content = gemini.generate_all(mixed_topics, batch_size=5)
            for entry in batch_content:
                content_dict = {
                    "topic": entry.get("topic", ""),
                    "x_thread": entry.get("x_thread", ""),
                    "x_post": entry.get("x_post", ""),
                    "linkedin_post": entry.get("linkedin_post", ""),
                    "instagram_caption": entry.get("instagram_caption", ""),
                    "carousel_outline": entry.get("carousel_outline", ""),
                    "content_type": "Mixed Content",
                }
                sheets.write_single_content(content_dict)
                mixed_content.append(content_dict)
        except Exception as e:
            logger.error(f"[MIXED] Batch generation failed: {e}", exc_info=True)
            print(f"❌ MIXED batch failed: {e}")
            for topic in mixed_topics:
                log_failure(topic, "Mixed Content", str(e))
                sheets.write_failed_topic(topic, "Mixed Content", str(e))

    if mixed_content:
        save_to_json(mixed_content, f"mixed_content_{timestamp}.json")

    # ============================================================
    # STEP 8: SHORT POSTS (Rows 162-201)
    # ============================================================
    short_topics = get_topics_by_range(topics_data, *DISTRIBUTION["short_posts"])
    print(f"\n⚡ Step 8: Generating {len(short_topics)} short posts (Rows 162-201)...")

    for topic in short_topics:
        logger.info(f"[SHORT POST] Generating for '{topic}'")
        try:
            x_prompt = get_short_post_prompt(topic, "x")
            gemini._rate_limit_wait()
            x_post_text = gemini.model.generate_content(x_prompt).text.strip()

            ig_prompt = get_short_post_prompt(topic, "instagram")
            gemini._rate_limit_wait()
            ig_caption_text = gemini.model.generate_content(ig_prompt).text.strip()

            content_dict = {
                "topic": topic,
                "x_thread": "",
                "x_post": x_post_text,
                "linkedin_post": "",
                "instagram_caption": ig_caption_text,
                "carousel_outline": "",
                "content_type": "Short Post",
            }

            sheets.write_single_content(content_dict)
            short_content.append(content_dict)
            logger.info(f"[SHORT POST] ✅ Success for '{topic}'")
        except Exception as e:
            logger.error(f"[SHORT POST] Error for '{topic}': {e}", exc_info=True)
            print(f"❌ SHORT POST failed for '{topic}': {e}")
            log_failure(topic, "Short Post", str(e))
            sheets.write_failed_topic(topic, "Short Post", str(e))

    if short_content:
        save_to_json(short_content, f"short_posts_{timestamp}.json")

    # ============================================================
    # FINAL STATUS UPDATES & SUMMARY
    # ============================================================
    all_content = (
        carousel_content_1
        + thread_content
        + carousel_content_2
        + linkedin_content
        + x_post_content
        + ig_content
        + mixed_content
        + short_content
    )

    for item in all_content:
        if item.get("topic"):
            sheets.update_topic_status(item["topic"], "Generated")

    failures = get_failure_summary()
    total_carousels = len(carousel_content_1) + len(carousel_content_2)

    print("\n" + "=" * 60)
    print("📊 GENERATION COMPLETE")
    print("=" * 60)
    print(f"🎨 Carousels (Rows 2-31): {len(carousel_content_1)}")
    print(f"🧵 X Threads: {len(thread_content)}")
    print(f"🎨 Carousels (Rows 52-71): {len(carousel_content_2)}")
    print(f"💼 LinkedIn Posts: {len(linkedin_content)}")
    print(f"🐦 X Posts: {len(x_post_content)}")
    print(f"📸 Instagram Captions: {len(ig_content)}")
    print(f"🎯 Mixed Content (all formats): {len(mixed_content)}")
    print(f"⚡ Short Posts (X + IG): {len(short_content)}")
    print(f"\n📈 TOTAL CAROUSELS: {total_carousels}")
    print(f"📝 TOTAL TEXT PIECES: {len(all_content)}")

    if failures:
        print(f"\n⚠️ FAILURES: {len(failures)}")
        failure_counts = Counter(f["content_type"] for f in failures)
        for content_type, count in failure_counts.items():
            print(f"   - {content_type}: {count}")
        print("\n❌ Failed topics logged to 'Failed' sheet")
        print("📄 Check logs/run.log for detailed errors")
    else:
        print("\n🎉 NO FAILURES - All content generated successfully!")

    print("\n✅ All content saved to:")
    print("   - Google Sheets (Generated_Posts tab)")
    print("   - output/posts/*.json")
    print("   - logs/run.log")
    print("=" * 60)


if __name__ == "__main__":
    main()

