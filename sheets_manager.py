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
            # Handle carousel content (has linkedin_carousel and instagram_carousel)
            carousel_outline = content.get("carousel_outline", "")
            if not carousel_outline:
                # Combine LinkedIn and Instagram carousels if present
                linkedin_carousel = content.get("linkedin_carousel", "")
                instagram_carousel = content.get("instagram_carousel", "")
                if linkedin_carousel or instagram_carousel:
                    carousel_outline = f"LinkedIn:\n{linkedin_carousel}\n\nInstagram:\n{instagram_carousel}"
            
            row = [
                content.get("topic", ""),
                content.get("x_thread", ""),
                content.get("x_post", ""),
                content.get("linkedin_post", ""),
                content.get("instagram_caption", ""),
                carousel_outline,
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
    
    def write_failed_topic(self, topic, content_type, error_message):
        """
        Log a failed topic to the Failed sheet.
        
        Args:
            topic: Topic that failed
            content_type: Type of content (e.g., "X Thread", "Video", "Carousel")
            error_message: Error description
        """
        try:
            # Try to get Failed sheet, create if doesn't exist
            try:
                failed_sheet = self.sheet.worksheet("Failed")
            except:
                # Create Failed sheet with headers
                failed_sheet = self.sheet.add_worksheet(title="Failed", rows=1000, cols=5)
                failed_sheet.append_row([
                    "Timestamp",
                    "Topic",
                    "Content Type",
                    "Error Message",
                    "Status"
                ])
                print("✅ Created 'Failed' sheet")
            
            # Get current timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write failed entry
            failed_sheet.append_row([
                timestamp,
                topic,
                content_type,
                str(error_message)[:500],  # Truncate long errors
                "Pending Retry"
            ])
            
            print(f"📝 Logged failure: {topic} ({content_type})")
            
        except Exception as e:
            print(f"⚠️ Could not log failure to sheet: {e}")
    
    def get_failed_topics(self, status="Pending Retry"):
        """
        Get topics from Failed sheet that need retry.
        
        Args:
            status: Filter by status (default: "Pending Retry")
        
        Returns:
            List of failed topic dictionaries
        """
        try:
            failed_sheet = self.sheet.worksheet("Failed")
            data = failed_sheet.get_all_records()
            
            # Filter by status
            failed_topics = [
                row for row in data 
                if row.get("Status", "") == status
            ]
            
            return failed_topics
        except:
            print("⚠️ No Failed sheet found or empty")
            return []
    
    def mark_retry_complete(self, topic, content_type):
        """
        Mark a failed topic as successfully retried.
        
        Args:
            topic: Topic that was retried
            content_type: Content type that succeeded
        """
        try:
            failed_sheet = self.sheet.worksheet("Failed")
            
            # Find the row
            cell = failed_sheet.find(topic)
            if cell:
                # Update status column (column E = 5)
                failed_sheet.update_cell(cell.row, 5, "Retry Success")
                print(f"✅ Marked retry success: {topic}")
        except Exception as e:
            print(f"⚠️ Could not update retry status: {e}")

