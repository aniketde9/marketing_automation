"""
Main automation script for marketing content generation.
"""
import sys
from sheets_manager import SheetsManager
from gemini_generator import GeminiGenerator
from sora_generator import SoraGenerator
from utils import save_to_json, format_timestamp, print_summary


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("🚀 MARKETING AUTOMATION BOT")
    print("="*60 + "\n")
    
    # Initialize managers
    try:
        sheets = SheetsManager()
        gemini = GeminiGenerator()
        sora = SoraGenerator()
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        sys.exit(1)
    
    # Step 1: Fetch topics from Google Sheets
    print("\n📋 Step 1: Fetching topics from Google Sheets...")
    topics_data = sheets.get_topics(limit=100, status="Pending")
    
    if not topics_data:
        print("❌ No pending topics found. Add topics to your Google Sheet.")
        sys.exit(1)
    
    topics_list = [row["Topic"] for row in topics_data if row.get("Topic")]
    print(f"✅ Loaded {len(topics_list)} topics")
    
    # Step 2: Generate text content with Gemini
    print("\n📝 Step 2: Generating content with Gemini 3.0...")
    generated_content = gemini.generate_all(topics_list, batch_size=5)
    
    if not generated_content:
        print("❌ Content generation failed")
        sys.exit(1)
    
    # Save generated content to JSON
    timestamp = format_timestamp()
    save_to_json(generated_content, f"generated_content_{timestamp}.json")
    
    # Step 3: Write to Google Sheets
    print("\n📊 Step 3: Writing content to Google Sheets...")
    sheets.write_generated_content(generated_content)
    
    # Update topic statuses
    for content in generated_content:
        sheets.update_topic_status(content["topic"], "Generated")
    
    # Step 4: Generate videos with Sora (optional)
    generate_videos = input("\n🎬 Generate videos with Sora? (y/n): ").lower()
    
    videos = []
    if generate_videos == 'y':
        num_videos = int(input("How many videos? (max 30): "))
        num_videos = min(num_videos, 30)
        
        # Use first N topics for video generation (will be distributed across video types)
        video_topics = topics_list[:num_videos]
        
        print(f"\n🎬 Step 4: Generating {num_videos} videos with Sora...")
        videos = sora.generate_batch(video_topics)
        
        # Save video info
        save_to_json(videos, f"videos_{timestamp}.json")
        
        # Write to Google Sheets
        for video in videos:
            sheets.write_video_info(video)
    
    # Print summary
    print_summary(generated_content, videos)
    
    print("\n✅ Automation complete! Check your Google Sheet and output/ folder.")


if __name__ == "__main__":
    main()

