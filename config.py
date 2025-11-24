"""
Configuration settings for the marketing automation bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Rate Limits
GEMINI_RPM = int(os.getenv("GEMINI_RPM", 2))  # Gemini 3.0: 2 requests per minute
GEMINI_RPD = int(os.getenv("GEMINI_RPD", 50))  # Gemini 3.0: 50 requests per day
SORA_DAILY_LIMIT = int(os.getenv("SORA_DAILY_LIMIT", 30))

# Model Configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-exp-1206")  # Gemini 3.0
SORA_DURATION = int(os.getenv("SORA_DURATION", 15))  # 15 seconds
SORA_RESOLUTION = os.getenv("SORA_RESOLUTION", "720p")

# Google Sheets Configuration
SHEETS_CONFIG = {
    "topics_sheet": "Topics",
    "generated_sheet": "Generated_Posts",
    "videos_sheet": "Videos",
    "schedule_sheet": "Schedule"
}

# Content Generation Settings
BATCH_SIZE = 5  # Generate 5 posts per API request
CONTENT_TYPES = ["x_thread", "x_post", "linkedin_post", "instagram_caption", "carousel_outline"]

# Output Paths
OUTPUT_DIR = "output"
POSTS_DIR = os.path.join(OUTPUT_DIR, "posts")
VIDEOS_DIR = os.path.join(OUTPUT_DIR, "videos")

# Create output directories if they don't exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not GOOGLE_SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID not found in .env file")
if not os.path.exists("credentials.json"):
    raise ValueError("credentials.json not found in project directory")

print("✅ Configuration loaded successfully")




