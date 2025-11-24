"""
Sora 2 API handler for video generation.
VERIFIED against official OpenAI documentation.
"""
import openai
import time
from config import OPENAI_API_KEY, SORA_DURATION
from prompts import get_video_prompt, VIDEO_TYPES
from utils import logger


class SoraGenerator:
    def __init__(self):
        """Initialize Sora client."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        logger.info("✅ Sora client initialized")
        print("✅ Sora client initialized")
    
    def generate_video(self, topic, video_type="educational"):
        """
        Generate a single video with Sora API.
        
        Args:
            topic: Topic for video
            video_type: 'educational', 'viral', or 'promotional'
        
        Returns:
            Dictionary with video info
        """
        try:
            prompt = get_video_prompt(topic, video_type)
            
            logger.info(f"[SORA] Queueing {video_type} video for topic: {topic[:50]}")
            print(f"🎬 Queueing: {topic[:50]}...")
            
            # CORRECT PARAMETERS (verified from official docs)
            response = self.client.videos.create(
                model="sora-2",
                prompt=prompt,
                seconds=str(SORA_DURATION)  # Must be string, not int
            )
            
            video_id = response.id
            logger.info(f"[SORA] Video queued - ID: {video_id}, Type: {video_type}")
            print(f"✅ Queued: {video_id}")
            
            # 1 MINUTE COOLDOWN
            logger.info("😴 Cooldown: waiting 60s...")
            print("😴 Cooldown: waiting 60s...")
            time.sleep(60)
            
            return {
                "video_id": video_id,
                "prompt": prompt,
                "topic": topic,
                "type": video_type,
                "status": "queued"
            }
            
        except Exception as e:
            logger.error(f"[SORA] Error queueing video for '{topic}': {e}", exc_info=True)
            print(f"❌ SORA error for {topic}: {e}")
            return None
    
    def check_video_status(self, video_id):
        """Check status and download video if complete."""
        try:
            # Retrieve video status
            response = self.client.videos.retrieve(video_id)
            
            if response.status == "completed":
                # Download video content using official method
                logger.info(f"[SORA] Downloading video {video_id}...")
                content = self.client.videos.download_content(video_id, variant="video")
                
                return {
                    "status": "completed",
                    "video_id": video_id,
                    "content": content  # This is a file-like object
                }
            else:
                return {
                    "status": response.status,
                    "video_id": video_id
                }
                
        except Exception as e:
            logger.error(f"[SORA] Error checking status for {video_id}: {e}", exc_info=True)
            return {"status": "error", "video_id": video_id}
    
    def generate_batch(self, topics_list):
        """Generate videos for batch of topics."""
        video_prompts = []
        topic_index = 0
        
        # Distribute across video types
        for video_type, count in VIDEO_TYPES.items():
            for i in range(count):
                if topic_index < len(topics_list):
                    video_prompts.append({
                        "topic": topics_list[topic_index],
                        "type": video_type
                    })
                    topic_index += 1
        
        print(f"\n🎬 Queueing {len(video_prompts)} videos (60s cooldown between each)...")
        logger.info(f"[SORA BATCH] Starting batch with {len(video_prompts)} videos")
        
        # Queue all videos
        video_ids = []
        for idx, video_prompt in enumerate(video_prompts, 1):
            print(f"\n[{idx}/{len(video_prompts)}] Queueing next video...")
            video_info = self.generate_video(
                topic=video_prompt["topic"],
                video_type=video_prompt["type"]
            )
            if video_info:
                video_ids.append(video_info)
        
        print(f"\n✅ Queued {len(video_ids)} videos. Polling for completion...")
        logger.info(f"[SORA BATCH] Queued {len(video_ids)} videos")
        
        # Poll until complete
        completed_videos = []
        poll_attempts = 0
        max_polls = 120  # Max 2 hours
        
        while video_ids and poll_attempts < max_polls:
            poll_attempts += 1
            print(f"\n⏳ Poll #{poll_attempts}: Checking {len(video_ids)} videos...")
            
            for video_info in video_ids[:]:
                status_info = self.check_video_status(video_info["video_id"])
                
                if status_info["status"] == "completed":
                    # Save video to file
                    filename = f"{video_info['video_id']}.mp4"
                    filepath = f"output/videos/{filename}"
                    
                    try:
                        # Use the official write_to_file method
                        status_info["content"].write_to_file(filepath)
                        
                        completed_videos.append({
                            **video_info,
                            "status": "completed",
                            "filepath": filepath
                        })
                        video_ids.remove(video_info)
                        logger.info(f"[SORA] ✅ Saved: {filename}")
                        print(f"✅ Saved: {filename}")
                        
                    except Exception as e:
                        logger.error(f"[SORA] Error saving {filename}: {e}", exc_info=True)
                        print(f"❌ Error saving {filename}: {e}")
                        video_ids.remove(video_info)
                        
                elif status_info["status"] == "error" or status_info["status"] == "failed":
                    logger.error(f"[SORA] ❌ Video failed: {video_info['video_id']}")
                    print(f"❌ Video failed: {video_info['video_id']}")
                    video_ids.remove(video_info)
                else:
                    # Still in progress
                    logger.info(f"[SORA] Video {video_info['video_id']}: {status_info['status']}")
            
            if video_ids:
                print(f"⏳ {len(video_ids)} videos still processing. Waiting 30s...")
                time.sleep(30)
        
        if poll_attempts >= max_polls:
            logger.warning(f"[SORA] Max polls reached. {len(video_ids)} still pending")
            print(f"⚠️ Max polling reached. {len(video_ids)} videos still pending")
        
        logger.info(f"[SORA BATCH] Complete. Generated: {len(completed_videos)} videos")
        print(f"\n✅ Batch complete. Generated {len(completed_videos)} videos")
        
        return completed_videos
