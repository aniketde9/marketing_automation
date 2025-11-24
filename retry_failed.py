"""
Retry script for failed topics.
Run this after main.py to retry only the topics that failed.
"""
import sys
from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from sora_generator import SoraGenerator
from utils import logger, save_to_json, format_timestamp


def retry_failed():
    """Retry all failed topics from the Failed sheet."""
    print("\n" + "="*60)
    print("🔄 RETRYING FAILED TOPICS")
    print("="*60 + "\n")
    
    # Initialize
    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
        sora = SoraGenerator()
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        sys.exit(1)
    
    # Get failed topics
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
            # Route to correct generator based on content type
            if "Thread" in content_type:
                from prompts import get_thread_prompt
                gemini._rate_limit_wait()
                prompt = get_thread_prompt(topic)
                result = gemini.model.generate_content(prompt)
                thread_text = result.text.strip()
                
                retried_content.append({
                    "topic": topic,
                    "x_thread": thread_text,
                    "content_type": "X Thread"
                })
                
            elif "Carousel" in content_type:
                from prompts import get_carousel_prompt
                
                gemini._rate_limit_wait()
                linkedin = gemini.model.generate_content(
                    get_carousel_prompt(topic, "linkedin")
                ).text.strip()
                
                gemini._rate_limit_wait()
                instagram = gemini.model.generate_content(
                    get_carousel_prompt(topic, "instagram")
                ).text.strip()
                
                retried_content.append({
                    "topic": topic,
                    "linkedin_carousel": linkedin,
                    "instagram_carousel": instagram,
                    "content_type": "Carousel"
                })
                
            elif "Video" in content_type:
                video = sora.generate_video(topic, "educational")
                if video and video.get("status") == "queued":
                    retried_content.append(video)
                else:
                    raise Exception("Video generation failed")
                    
            elif "LinkedIn" in content_type:
                from prompts import get_linkedin_prompt
                gemini._rate_limit_wait()
                prompt = get_linkedin_prompt(topic)
                result = gemini.model.generate_content(prompt)
                post_text = result.text.strip()
                
                retried_content.append({
                    "topic": topic,
                    "linkedin_post": post_text,
                    "content_type": "LinkedIn Post"
                })
                
            elif "X Post" in content_type:
                from prompts import get_short_post_prompt
                gemini._rate_limit_wait()
                prompt = get_short_post_prompt(topic, "x")
                result = gemini.model.generate_content(prompt)
                post_text = result.text.strip()
                
                retried_content.append({
                    "topic": topic,
                    "x_post": post_text,
                    "content_type": "X Post"
                })
                
            elif "Instagram" in content_type:
                from prompts import get_short_post_prompt
                gemini._rate_limit_wait()
                prompt = get_short_post_prompt(topic, "instagram")
                result = gemini.model.generate_content(prompt)
                caption_text = result.text.strip()
                
                retried_content.append({
                    "topic": topic,
                    "instagram_caption": caption_text,
                    "content_type": "Instagram Caption"
                })
                
            elif "Short Post" in content_type:
                from prompts import get_short_post_prompt
                
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
                
                retried_content.append({
                    "topic": topic,
                    "x_post": x_text,
                    "instagram_caption": ig_text,
                    "content_type": "Short Post"
                })
                
            elif "Mixed" in content_type:
                # Retry as batch
                mixed_result = gemini.generate_all([topic], batch_size=1)
                if mixed_result:
                    retried_content.extend(mixed_result)
                else:
                    raise Exception("Mixed content generation failed")
            
            # Mark as successful
            sheets.mark_retry_complete(topic, content_type)
            print(f"✅ Success: {topic}")
            logger.info(f"[RETRY] Successfully retried {content_type} for topic: {topic}")
            
        except Exception as e:
            logger.error(f"[RETRY] Still failed for '{topic}': {e}", exc_info=True)
            print(f"❌ Still failed: {topic} → {e}")
            continue
    
    # Save retried content
    if retried_content:
        save_to_json(retried_content, f"retried_{timestamp}.json")
        sheets.write_generated_content(retried_content)
        
        # Update topic statuses
        for item in retried_content:
            if "topic" in item:
                sheets.update_topic_status(item["topic"], "Generated")
    
    print(f"\n✅ Retry complete. Successfully retried: {len(retried_content)}/{len(failed_topics)}")


if __name__ == "__main__":
    retry_failed()

