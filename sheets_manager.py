"""
Google Sheets manager for reading/writing content.
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from config import GOOGLE_SHEET_ID, SHEETS_CONFIG


class SheetsManager:
    def __init__(self):
        """Initialize Google Sheets connection."""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(GOOGLE_SHEET_ID)
        print("✅ Connected to Google Sheets")
    
    def get_topics(self, limit=100, status="Pending"):
        """
        Get topics from Topics sheet.
        
        Args:
            limit: Maximum number of topics to fetch
            status: Filter by status (default: "Pending")
        
        Returns:
            List of topic dictionaries
        """
        topics_sheet = self.sheet.worksheet(SHEETS_CONFIG["topics_sheet"])
        data = topics_sheet.get_all_records()
        
        # Filter by status if provided
        if status:
            data = [row for row in data if row.get("Status", "Pending") == status]
        
        return data[:limit]
    
    def write_generated_content(self, content_list):
        """
        Write generated content to Generated_Posts sheet.
        
        Args:
            content_list: List of dictionaries with generated content
        """
        generated_sheet = self.sheet.worksheet(SHEETS_CONFIG["generated_sheet"])
        
        # Prepare rows for batch insert
        rows = []
        for content in content_list:
            row = [
                content.get("topic", ""),
                content.get("x_thread", ""),
                content.get("x_post", ""),
                content.get("linkedin_post", ""),
                content.get("instagram_caption", ""),
                content.get("carousel_outline", ""),
                "Generated"
            ]
            rows.append(row)
        
        # Append all rows at once
        if rows:
            generated_sheet.append_rows(rows)
            print(f"✅ Wrote {len(rows)} generated posts to sheet")
    
    def update_topic_status(self, topic, status="Generated"):
        """
        Update status of a topic in Topics sheet.
        
        Args:
            topic: Topic text to find
            status: New status value
        """
        topics_sheet = self.sheet.worksheet(SHEETS_CONFIG["topics_sheet"])
        cell = topics_sheet.find(topic)
        if cell:
            topics_sheet.update_cell(cell.row, 3, status)  # Column C = Status
    
    def write_video_info(self, video_data):
        """
        Write video generation info to Videos sheet.
        
        Args:
            video_data: Dictionary with video details
        """
        videos_sheet = self.sheet.worksheet(SHEETS_CONFIG["videos_sheet"])
        row = [
            video_data.get("topic", ""),
            video_data.get("type", ""),
            video_data.get("prompt", ""),
            video_data.get("video_id", ""),
            video_data.get("status", ""),
            video_data.get("url", ""),
            video_data.get("duration", "")
        ]
        videos_sheet.append_row(row)
        print(f"✅ Logged video: {video_data.get('video_id')}")

