"""
Main automation script with row-based content distribution.
"""
import sys
from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from sora_generator import SoraGenerator
from utils import (
    save_to_json, 
    format_timestamp, 
    print_summary, 
    logger,
    log_failure,
    get_failure_summary,
    clear_failures
)

# ============================================================
# ROW-BASED DISTRIBUTION STRATEGY
# ============================================================

DISTRIBUTION = {
    "videos": (2, 31),              # Rows 2-31: 30 videos
    "x_threads": (32, 51),          # Rows 32-51: 20 threads
    "carousels": (52, 71),          # Rows 52-71: 20 carousels
    "linkedin_posts": (72, 91),     # Rows 72-91: 20 LinkedIn posts
    "x_posts": (92, 111),           # Rows 92-111: 20 X posts
    "instagram_captions": (112, 151), # Rows 112-151: 40 IG captions
    "mixed_all": (152, 161),        # Rows 152-161: 10 all formats
    "short_posts": (162, 201)       # Rows 162-201: 40 short posts
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
    # topics_data is 0-indexed, but rows start at 2 in sheet
    # So row 2 = index 0, row 3 = index 1, etc.
    start_idx = start_row - 2
    end_idx = end_row - 2 + 1  # +1 because range is inclusive
    
    return [row["Topic"] for row in topics_data[start_idx:end_idx] if row.get("Topic")]


def main():
    """Main execution with row-based distribution."""
    print("\n" + "="*60)
    print("🚀 MARKETING AUTOMATION BOT")
    print("="*60 + "\n")
    
    # Initialize
    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
        sora = SoraGenerator()
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        sys.exit(1)
    
    # Fetch all topics
    print("\n📋 Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=200, status="Pending")
    
    if len(topics_data) < 200:
        print(f"⚠️ Warning: Only {len(topics_data)} topics found. Expected 200.")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != 'y':
            sys.exit(0)
    
    print(f"✅ Loaded {len(topics_data)} topics")
    
    # Clear failure log for fresh run
    clear_failures()
    
    # Initialize timestamp for all saves
    timestamp = format_timestamp()
    
    # ============================================================
    # STEP 1: GENERATE VIDEOS (Rows 2-31)
    # ============================================================
    
    video_topics = get_topics_by_range(topics_data, *DISTRIBUTION["videos"])
    print(f"\n🎬 Step 1: Generating {len(video_topics)} videos (Rows 2-31)...")
    
    videos = []
    if video_topics:
        logger.info(f"[VIDEO] Starting video generation for {len(video_topics)} topics")
        
        try:
            # Pass sheets_manager for immediate writes
            videos = sora.generate_batch(video_topics, sheets_manager=sheets)
            
            # Check which topics failed
            successful_topics = [v.get("topic") for v in videos if v.get("status") == "completed" and v.get("topic")]
            failed_topics = set(video_topics) - set(successful_topics)
            
            for topic in failed_topics:
                log_failure(topic, "Video", "Video generation failed or timed out")
                sheets.write_failed_topic(topic, "Video", "Video generation failed or timed out")
            
            # Videos are already written to sheet immediately by sora_generator
            # Just save JSON backup
            save_to_json(videos, f"videos_{timestamp}.json")
                    
        except Exception as e:
            logger.error(f"[VIDEO] Batch generation failed: {e}", exc_info=True)
            print(f"❌ Video batch failed: {e}")
            
            # Mark all video topics as failed
            for topic in video_topics:
                log_failure(topic, "Video", f"Batch error: {str(e)}")
                sheets.write_failed_topic(topic, "Video", f"Batch error: {str(e)}")
    
    # ============================================================
    # STEP 2: GENERATE X THREADS (Rows 32-51)
    # ============================================================
    
    thread_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_threads"])
    print(f"\n🧵 Step 2: Generating {len(thread_topics)} X threads (Rows 32-51)...")
    
    thread_content = []
    if thread_topics:
        from prompts import get_thread_prompt
        
        for topic in thread_topics:
            logger.info(f"[THREAD] Generating X thread for topic: {topic}")
            try:
                gemini._rate_limit_wait()
                prompt = get_thread_prompt(topic)
                # Call Gemini for individual thread
                response = gemini.model.generate_content(prompt)
                thread_text = response.text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": thread_text,
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "X Thread"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                thread_content.append(content_dict)
                
                logger.info(f"[THREAD] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[THREAD] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ THREAD failed for topic: {topic} → {e}")
                
                # Log to failure tracker
                log_failure(topic, "X Thread", str(e))
                sheets.write_failed_topic(topic, "X Thread", str(e))
                
                # continue automatically to next topic
                continue
        
        # Save JSON backup
        if thread_content:
            save_to_json(thread_content, f"x_threads_{timestamp}.json")
    
    # ============================================================
    # STEP 3: GENERATE CAROUSELS (Rows 52-71)
    # ============================================================
    
    carousel_topics = get_topics_by_range(topics_data, *DISTRIBUTION["carousels"])
    print(f"\n📊 Step 3: Generating {len(carousel_topics)} carousels (Rows 52-71)...")
    
    carousel_content = []
    if carousel_topics:
        from prompts import get_carousel_prompt
        
        for topic in carousel_topics:
            logger.info(f"[CAROUSEL] Generating carousel for topic: {topic}")
            try:
                # Generate for both platforms
                linkedin_prompt = get_carousel_prompt(topic, "linkedin")
                instagram_prompt = get_carousel_prompt(topic, "instagram")
                
                gemini._rate_limit_wait()
                linkedin_carousel = gemini.model.generate_content(linkedin_prompt).text.strip()
                
                gemini._rate_limit_wait()
                instagram_carousel = gemini.model.generate_content(instagram_prompt).text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "linkedin_carousel": linkedin_carousel,
                    "instagram_carousel": instagram_carousel,
                    "content_type": "Carousel"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                carousel_content.append(content_dict)
                
                logger.info(f"[CAROUSEL] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[CAROUSEL] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ CAROUSEL failed for topic: {topic} → {e}")
                
                log_failure(topic, "Carousel", str(e))
                sheets.write_failed_topic(topic, "Carousel", str(e))
                
                continue
        
        # Save JSON backup
        if carousel_content:
            save_to_json(carousel_content, f"carousels_{timestamp}.json")
    
    # ============================================================
    # STEP 4: GENERATE LINKEDIN POSTS (Rows 72-91)
    # ============================================================
    
    linkedin_topics = get_topics_by_range(topics_data, *DISTRIBUTION["linkedin_posts"])
    print(f"\n💼 Step 4: Generating {len(linkedin_topics)} LinkedIn posts (Rows 72-91)...")
    
    linkedin_content = []
    if linkedin_topics:
        from prompts import get_linkedin_prompt
        
        for topic in linkedin_topics:
            logger.info(f"[LINKEDIN] Generating LinkedIn post for topic: {topic}")
            try:
                gemini._rate_limit_wait()
                prompt = get_linkedin_prompt(topic)
                post_text = gemini.model.generate_content(prompt).text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": post_text,
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "LinkedIn Post"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                linkedin_content.append(content_dict)
                
                logger.info(f"[LINKEDIN] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[LINKEDIN] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ LINKEDIN POST failed for topic: {topic} → {e}")
                
                log_failure(topic, "LinkedIn Post", str(e))
                sheets.write_failed_topic(topic, "LinkedIn Post", str(e))
                
                continue
        
        # Save JSON backup
        if linkedin_content:
            save_to_json(linkedin_content, f"linkedin_posts_{timestamp}.json")
    
    # ============================================================
    # STEP 5: GENERATE X POSTS (Rows 92-111)
    # ============================================================
    
    x_post_topics = get_topics_by_range(topics_data, *DISTRIBUTION["x_posts"])
    print(f"\n🐦 Step 5: Generating {len(x_post_topics)} X posts (Rows 92-111)...")
    
    x_post_content = []
    if x_post_topics:
        from prompts import get_short_post_prompt
        
        for topic in x_post_topics:
            logger.info(f"[X POST] Generating X post for topic: {topic}")
            try:
                gemini._rate_limit_wait()
                prompt = get_short_post_prompt(topic, "x")
                response = gemini.model.generate_content(prompt)
                post_text = response.text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": post_text,
                    "linkedin_post": "",
                    "instagram_caption": "",
                    "carousel_outline": "",
                    "content_type": "X Post"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                x_post_content.append(content_dict)
                
                logger.info(f"[X POST] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[X POST] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ X POST failed for topic: {topic} → {e}")
                
                log_failure(topic, "X Post", str(e))
                sheets.write_failed_topic(topic, "X Post", str(e))
                
                continue
        
        # Save JSON backup
        if x_post_content:
            save_to_json(x_post_content, f"x_posts_{timestamp}.json")
    
    # ============================================================
    # STEP 6: GENERATE INSTAGRAM CAPTIONS (Rows 112-151)
    # ============================================================
    
    ig_topics = get_topics_by_range(topics_data, *DISTRIBUTION["instagram_captions"])
    print(f"\n📸 Step 6: Generating {len(ig_topics)} Instagram captions (Rows 112-151)...")
    
    ig_content = []
    if ig_topics:
        from prompts import get_short_post_prompt
        
        for topic in ig_topics:
            logger.info(f"[INSTAGRAM] Generating Instagram caption for topic: {topic}")
            try:
                gemini._rate_limit_wait()
                prompt = get_short_post_prompt(topic, "instagram")
                response = gemini.model.generate_content(prompt)
                caption_text = response.text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": "",
                    "linkedin_post": "",
                    "instagram_caption": caption_text,
                    "carousel_outline": "",
                    "content_type": "Instagram Caption"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                ig_content.append(content_dict)
                
                logger.info(f"[INSTAGRAM] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[INSTAGRAM] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ INSTAGRAM CAPTION failed for topic: {topic} → {e}")
                
                log_failure(topic, "Instagram Caption", str(e))
                sheets.write_failed_topic(topic, "Instagram Caption", str(e))
                
                continue
        
        # Save JSON backup
        if ig_content:
            save_to_json(ig_content, f"instagram_captions_{timestamp}.json")
    
    # ============================================================
    # STEP 7: GENERATE MIXED (ALL FORMATS) (Rows 152-161)
    # ============================================================
    
    mixed_topics = get_topics_by_range(topics_data, *DISTRIBUTION["mixed_all"])
    print(f"\n🎯 Step 7: Generating ALL formats for {len(mixed_topics)} topics (Rows 152-161)...")
    
    mixed_content = []
    if mixed_topics:
        logger.info(f"[MIXED] Generating all formats for {len(mixed_topics)} topics")
        
        try:
            # This returns a list of content dicts with all 5 formats
            batch_content = gemini.generate_all(mixed_topics, batch_size=5)
            
            # Write each one to sheet immediately
            for content_dict in batch_content:
                # Ensure content_type is set
                if "content_type" not in content_dict:
                    content_dict["content_type"] = "Mixed Content"
                
                sheets.write_single_content(content_dict)
                mixed_content.append(content_dict)
            
            logger.info(f"[MIXED] ✅ Generated and wrote {len(batch_content)} mixed content pieces")
            
            # Check for failed topics in mixed content
            successful_topics = [c.get("topic") for c in mixed_content if c.get("topic")]
            failed_topics = set(mixed_topics) - set(successful_topics)
            
            for topic in failed_topics:
                log_failure(topic, "Mixed Content", "Batch generation failed")
                sheets.write_failed_topic(topic, "Mixed Content", "Batch generation failed")
                
        except Exception as e:
            logger.error(f"[MIXED] Batch generation failed: {e}", exc_info=True)
            print(f"❌ Mixed content batch failed: {e}")
            
            for topic in mixed_topics:
                log_failure(topic, "Mixed Content", f"Batch error: {str(e)}")
                sheets.write_failed_topic(topic, "Mixed Content", f"Batch error: {str(e)}")
        
        # Save JSON backup
        if mixed_content:
            save_to_json(mixed_content, f"mixed_content_{timestamp}.json")
    
    # ============================================================
    # STEP 8: GENERATE SHORT POSTS (Rows 162-201)
    # ============================================================
    
    short_topics = get_topics_by_range(topics_data, *DISTRIBUTION["short_posts"])
    print(f"\n⚡ Step 8: Generating {len(short_topics)} short posts (Rows 162-201)...")
    
    short_content = []
    if short_topics:
        from prompts import get_short_post_prompt
        
        for topic in short_topics:
            logger.info(f"[SHORT POST] Generating short posts for topic: {topic}")
            try:
                # Generate both X post and IG caption for each
                x_prompt = get_short_post_prompt(topic, "x")
                ig_prompt = get_short_post_prompt(topic, "instagram")
                
                gemini._rate_limit_wait()
                x_response = gemini.model.generate_content(x_prompt)
                x_text = x_response.text.strip()
                
                gemini._rate_limit_wait()
                ig_response = gemini.model.generate_content(ig_prompt)
                ig_text = ig_response.text.strip()
                
                content_dict = {
                    "topic": topic,
                    "x_thread": "",
                    "x_post": x_text,
                    "linkedin_post": "",
                    "instagram_caption": ig_text,
                    "carousel_outline": "",
                    "content_type": "Short Post"
                }
                
                # WRITE TO SHEET IMMEDIATELY
                sheets.write_single_content(content_dict)
                
                # Also keep in memory for JSON backup
                short_content.append(content_dict)
                
                logger.info(f"[SHORT POST] ✅ Success for topic: {topic}")
                
            except Exception as e:
                logger.error(f"[SHORT POST] Error for topic '{topic}': {e}", exc_info=True)
                print(f"❌ SHORT POST failed for topic: {topic} → {e}")
                
                log_failure(topic, "Short Post", str(e))
                sheets.write_failed_topic(topic, "Short Post", str(e))
                
                continue
        
        # Save JSON backup
        if short_content:
            save_to_json(short_content, f"short_posts_{timestamp}.json")
    
    # ============================================================
    # STEP 9: UPDATE TOPIC STATUSES
    # ============================================================
    
    print("\n📊 Step 9: Updating topic statuses...")
    
    # All content has already been written to sheets immediately
    # Now just update the status in Topics sheet
    all_content = (
        thread_content + 
        carousel_content + 
        linkedin_content + 
        x_post_content + 
        ig_content + 
        mixed_content + 
        short_content
    )
    
    # Update statuses
    for item in all_content:
        if "topic" in item:
            sheets.update_topic_status(item["topic"], "Generated")
    
    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    
    total_posts = (
        len(thread_content) + 
        len(carousel_content) * 2 +  # Both LinkedIn and IG
        len(linkedin_content) + 
        len(x_post_content) + 
        len(ig_content) + 
        len(mixed_content) * 5 +  # 5 formats per mixed topic
        len(short_content) * 2  # X + IG per short topic
    )
    
    # Get failure summary
    failures = get_failure_summary()
    
    print("\n" + "="*60)
    print("📊 GENERATION COMPLETE")
    print("="*60)
    print(f"🎬 Videos: {len(videos)}")
    print(f"🧵 X Threads: {len(thread_content)}")
    print(f"📊 Carousels: {len(carousel_content)} sets (LinkedIn + Instagram)")
    print(f"💼 LinkedIn Posts: {len(linkedin_content)}")
    print(f"🐦 X Posts: {len(x_post_content)}")
    print(f"📸 Instagram Captions: {len(ig_content)}")
    print(f"🎯 Mixed Content: {len(mixed_content)} (all formats)")
    print(f"⚡ Short Posts: {len(short_content)} (X + IG)")
    print(f"\n🚀 TOTAL POSTS: {total_posts}")
    print(f"🎥 TOTAL VIDEO REPOSTS (5 platforms): {len(videos) * 5}")
    print(f"📈 GRAND TOTAL: {total_posts + (len(videos) * 5)}")
    
    # Failure Report
    if failures:
        print(f"\n⚠️  FAILURES: {len(failures)}")
        print("="*60)
        
        # Group by content type
        from collections import Counter
        failure_types = Counter([f["content_type"] for f in failures])
        
        for content_type, count in failure_types.items():
            print(f"   {content_type}: {count} failed")
        
        print(f"\n💾 Failed topics logged to 'Failed' sheet in Google Sheets")
        print(f"📄 Check logs/run.log for detailed error messages")
        
        # Save failures to JSON
        save_to_json(failures, f"failures_{timestamp}.json")
    else:
        print(f"\n✅ NO FAILURES - All content generated successfully!")
    
    print("="*60)
    
    logger.info(f"Run complete. Success: {total_posts} posts, {len(videos)} videos. Failures: {len(failures)}")
    
    print(f"\n✅ All content saved to:")
    print(f"   - Google Sheets (Generated_Posts tab)")
    print(f"   - Google Sheets (Failed tab) ← Re-run these")
    print(f"   - output/posts/*.json")
    print(f"   - output/videos/*.mp4")
    print(f"   - logs/run.log")


if __name__ == "__main__":
    main()
