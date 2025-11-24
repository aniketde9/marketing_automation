"""
Utility functions for the marketing automation bot.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import json
import requests
from datetime import datetime

# ==============================
# LOGGER SETUP (GLOBAL)
# ==============================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "run.log")

logger = logging.getLogger("marketing_bot")
logger.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# File handler (rotating)
fh = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5)
fh.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Attach handlers (avoid duplicates if re-imported)
if not logger.handlers:
    logger.addHandler(ch)
    logger.addHandler(fh)

logger.propagate = False

# Track all failures in memory during run
FAILURE_LOG = []


def log_failure(topic, content_type, error_message):
    """
    Log a failure both to logger and to in-memory tracker.
    
    Args:
        topic: Topic that failed
        content_type: Content type (e.g., "X Thread", "Video")
        error_message: Error description
    """
    failure_entry = {
        "topic": topic,
        "content_type": content_type,
        "error": str(error_message)
    }
    
    FAILURE_LOG.append(failure_entry)
    logger.error(f"[FAILURE] {content_type} failed for '{topic}': {error_message}")


def get_failure_summary():
    """Get summary of all failures in this run."""
    return FAILURE_LOG


def clear_failures():
    """Clear failure log (for fresh runs)."""
    global FAILURE_LOG
    FAILURE_LOG = []


def save_to_json(data, filename):
    """Save data to JSON file."""
    filepath = os.path.join("output/posts", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved JSON: {filepath}")
    print(f"💾 Saved to {filepath}")


def load_from_json(filename):
    """Load data from JSON file."""
    filepath = os.path.join("output/posts", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            logger.info(f"Loaded JSON: {filepath}")
            return json.load(f)
    logger.warning(f"JSON not found: {filepath}")
    return None


def format_timestamp():
    """Get formatted timestamp for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def download_video(url, filename):
    """Download video from URL to local file."""
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        filepath = os.path.join("output/videos", filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded video: {filepath}")
        print(f"💾 Downloaded: {filename}")
        return filepath
    except Exception as e:
        logger.error(f"Download failed for {filename}: {e}", exc_info=True)
        print(f"❌ Download failed for {filename}: {e}")
        return None


def print_summary(generated_content, videos):
    """Print generation summary."""
    logger.info(
        f"Summary - posts:{len(generated_content)}, videos:{len(videos)}, "
        f"text_pieces:{len(generated_content)*5}, video_reposts:{len(videos)*5}"
    )
    print("\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Posts generated: {len(generated_content)}")
    print(f"🎬 Videos generated: {len(videos)}")
    print(f"📝 Total content pieces: {len(generated_content) * 5}")  # 5 formats per post
    print(f"🎥 Video reposts (5 platforms): {len(videos) * 5}")
    print(f"🚀 Total posts across platforms: {(len(generated_content) * 5) + (len(videos) * 5)}")
    print("="*60)
