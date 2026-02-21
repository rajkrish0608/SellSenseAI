import logging
import random
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AdService:
    """
    Mock service for Meta/Google Ads API integration.
    """
    
    async def push_to_ads(self, campaign_id: int, creative_url: str, budget: float) -> str:
        """
        Simulates pushing a creative to Meta Ads Manager.
        Returns a mock Ad ID.
        """
        logger.info(f"Pushed creative {creative_url} to Meta Ads for campaign {campaign_id} with budget ${budget}")
        return f"act_{random.randint(100000, 999999)}"

    async def get_ad_metrics(self, ad_id: str) -> Dict[str, Any]:
        """
        Fetches mock performance metrics for a specific ad.
        """
        impressions = random.randint(1000, 5000)
        clicks = random.randint(50, 200)
        return {
            "ad_id": ad_id,
            "impressions": impressions,
            "clicks": clicks,
            "ctr": (clicks / impressions) * 100 if impressions > 0 else 0,
            "spend": random.uniform(5.0, 15.0)
        }

ad_service = AdService()
