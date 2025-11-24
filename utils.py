"""
Utility functions for the marketing automation bot.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "run.log")

logger = logging.getLogger("marketing_bot")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5)
fh.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(ch)
    logger.addHandler(fh)

logger.propagate = False

FAILURE_LOG = []


def log_failure(topic, content_type, error_message):
    """Log a failure both to logger and to in-memory tracker."""
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
