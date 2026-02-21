import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TrendService:
    """
    Service to fetch trending social media topics and audios.
    In production, this would use Apify, TikTok Research API, or Meta Graph API.
    """
    
    def get_market_trends(self) -> List[Dict[str, Any]]:
        # Mocking real-time market trends
        mock_trends = [
            {
                "name": "Brat Summer",
                "type": "topic",
                "source": "tiktok",
                "sentiment": "positive",
                "growth": "+450%"
            },
            {
                "name": "Original Sound - Cafe Jazz",
                "type": "audio",
                "source": "instagram",
                "sentiment": "neutral",
                "growth": "+120%"
            },
            {
                "name": "Personal Branding Tips",
                "type": "topic",
                "source": "linkedin",
                "sentiment": "professional",
                "growth": "+80%"
            },
            {
                "name": "AI Productivity Hacks",
                "type": "hashtag",
                "source": "x",
                "sentiment": "positive",
                "growth": "+300%"
            }
        ]
        
        # Shuffle to simulate changes
        random.shuffle(mock_trends)
        return mock_trends[:3]

trend_service = TrendService()
