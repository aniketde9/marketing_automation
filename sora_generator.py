"""
Sora API handler for video generation.
"""
import openai
import time
from config import OPENAI_API_KEY, SORA_DURATION, SORA_RESOLUTION
from prompts import get_video_prompt, VIDEO_TYPES
from utils import logger


openai.api_key = OPENAI_API_KEY


class SoraGenerator:
    def __init__(self):
        """Initialize Sora client."""
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print("✅ Sora client initialized")
    
    def generate_video(self, topic, video_type="educational"):
        """
        Generate a single video with Sora.
        
        Args:
            topic: Topic for video
            video_type: 'educational', 'viral', or 'promotional'
        
        Returns:
            Dictionary with video info
        """
        try:
            # Get customized prompt from prompts module
            prompt = get_video_prompt(topic, video_type)
            logger.info(f"[SORA] Queueing {video_type} video for topic: {topic}")
            
            print(f"🎬 Generating {video_type} video: {topic[:50]}...")
            
            response = self.client.videos.generate(
                model="sora-2",
                prompt=prompt,
                duration=f"{SORA_DURATION}s",
                resolution=SORA_RESOLUTION
            )
            
            video_id = response.id
            logger.info(f"[SORA] Queued video_id={video_id} type={video_type} topic={topic}")
            print(f"✅ Video queued: {video_id} ({video_type})")
            
            return {
                "video_id": video_id,
                "prompt": prompt,
                "topic": topic,
                "type": video_type,
                "status": "queued",
                "duration": SORA_DURATION
            }
            
        except Exception as e:
            logger.error(f"[SORA] Error queueing video for topic '{topic}': {e}", exc_info=True)
            print(f"❌ Sora API error: {e}")
            return None
    
    def check_video_status(self, video_id):
        """
        Check generation status of a video.
        
        Args:
            video_id: Video ID from generate_video
        
        Returns:
            Dictionary with status and URL if complete
        """
        try:
            response = self.client.videos.retrieve(video_id)
            status = response.status
            
            if status == "completed":
                return {
                    "status": "completed",
                    "url": response.url,
                    "video_id": video_id
                }
            else:
                return {
                    "status": status,
                    "video_id": video_id
                }
        except Exception as e:
            print(f"❌ Error checking video {video_id}: {e}")
            return {"status": "error", "video_id": video_id}
    
    def generate_batch(self, topics_list):
        """
        Generate videos based on VIDEO_TYPES distribution.
        
        Args:
            topics_list: List of topics (will use first 30)
        
        Returns:
            List of completed video info
        """
        video_prompts = []
        topic_index = 0
        
        # Distribute topics across video types
        for video_type, count in VIDEO_TYPES.items():
            for i in range(count):
                if topic_index < len(topics_list):
                    video_prompts.append({
                        "topic": topics_list[topic_index],
                        "type": video_type
                    })
                    topic_index += 1
        
        print(f"\n🎬 Video Distribution: {VIDEO_TYPES}")
        print(f"Queueing {len(video_prompts)} videos...")
        
        # Queue all videos
        video_ids = []
        for video_prompt in video_prompts:
            video_info = self.generate_video(
                topic=video_prompt["topic"],
                video_type=video_prompt["type"]
            )
            if video_info:
                video_ids.append(video_info)
            else:
                logger.warning(f"[SORA] Skipping failed video for topic: {video_prompt['topic']}")
            time.sleep(1)
        
        print(f"✅ {len(video_ids)} videos queued. Polling for completion...")
        
        # Poll until complete
        completed_videos = []
        while video_ids:
            for video_info in video_ids[:]:
                status_info = self.check_video_status(video_info["video_id"])
                
                if status_info["status"] == "completed":
                    completed_videos.append({**video_info, **status_info})
                    video_ids.remove(video_info)
                    logger.info(f"[SORA] Completed video_id={status_info['video_id']}")
                    print(f"✅ Video complete: {status_info['video_id']}")
                elif status_info["status"] == "error":
                    logger.error(f"[SORA] Video error for id={video_info['video_id']}")
                    video_ids.remove(video_info)
                    print(f"❌ Video failed: {video_info['video_id']}")
            
            if video_ids:
                print(f"⏳ Waiting for {len(video_ids)} videos... (polling in 30s)")
                time.sleep(30)
        
        print(f"✅ All videos complete. Generated: {len(completed_videos)}")
        return completed_videos

