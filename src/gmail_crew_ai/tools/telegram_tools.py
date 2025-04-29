import os
import requests
from pydantic import BaseModel, Field
from typing import Optional

class TelegramNotificationSchema(BaseModel):
    """Schema for TelegramNotificationTool input."""
    message: str = Field(..., description="The message content to send")

class TelegramNotificationTool:
    """Tool to send notifications via Telegram."""
    name: str = "telegram_notification"
    description: str = "Sends a notification to a specified Telegram chat"
    args_schema: type = TelegramNotificationSchema

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not self.token or not self.chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in the environment variables.")
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def _run(self, message: str) -> str:
        """Send a notification to a Telegram chat."""
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                return f"Notification sent successfully to chat ID {self.chat_id}"
            else:
                return f"Failed to send notification: {response.status_code}, {response.text}"
        except Exception as e:
            return f"Error sending notification: {str(e)}"