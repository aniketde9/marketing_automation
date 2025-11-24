"""
Configuration settings for the marketing automation bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Rate Limits
GEMINI_RPM = int(os.getenv("GEMINI_RPM", 15))  # Gemini 2.5 Flash-Lite: 15 RPM
GEMINI_RPD = int(os.getenv("GEMINI_RPD", 1000))  # Gemini 2.5 Flash-Lite: 1000 RPD

# Model Configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

# Google Sheets Configuration
SHEETS_CONFIG = {
    "topics_sheet": "Topics",
    "generated_sheet": "Generated_Posts",
    "schedule_sheet": "Schedule",
    "failed_sheet": "Failed"
}

# Content Generation Settings
BATCH_SIZE = 5  # Generate 5 posts per API request
CONTENT_TYPES = ["x_thread", "x_post", "linkedin_post", "instagram_caption", "carousel_outline"]

# Output Paths
OUTPUT_DIR = "output"
POSTS_DIR = os.path.join(OUTPUT_DIR, "posts")
LOGS_DIR = "logs"

# Create output directories if they don't exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Validation
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not GOOGLE_SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID not found in .env file")
if not os.path.exists("credentials.json"):
    raise ValueError("credentials.json not found in project directory")

print("Configuration loaded successfully")
print(f"   Gemini Model: {GEMINI_MODEL}")
print(f"   Gemini Rate Limits: {GEMINI_RPM} RPM, {GEMINI_RPD} RPD")
