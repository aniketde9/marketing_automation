"""
Utility functions for the marketing automation bot.
"""
import json
import os
from datetime import datetime


def save_to_json(data, filename):
    """Save data to JSON file."""
    filepath = os.path.join("output/posts", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {filepath}")


def load_from_json(filename):
    """Load data from JSON file."""
    filepath = os.path.join("output/posts", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def format_timestamp():
    """Get formatted timestamp for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def print_summary(generated_content, videos):
    """Print generation summary."""
    print("\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Posts generated: {len(generated_content)}")
    print(f"🎬 Videos generated: {len(videos)}")
    print(f"📝 Total content pieces: {len(generated_content) * 5}")  # 5 formats per post
    print(f"🎥 Video reposts (5 platforms): {len(videos) * 5}")
    print(f"🚀 Total posts across platforms: {(len(generated_content) * 5) + (len(videos) * 5)}")
    print("="*60)




