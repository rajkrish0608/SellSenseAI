import logging
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CompetitorService:
    """
    Mock service to simulate competitive intelligence gathering.
    Scans social mentions, ad libraries, and pricing.
    """
    
    def get_rival_activities(self, business_niche: str) -> List[Dict[str, Any]]:
        """
        Returns a list of recent activities from top competitors in the niche.
        """
        rivals = {
            "coffee": [
                {"name": "Starbucks Local", "action": "Flash Sale", "details": "30% off cold brews today", "impact": "High"},
                {"name": "Blue Tokai", "action": "New Launch", "details": "Monsoon Blend launched", "impact": "Medium"},
                {"name": "Third Wave", "action": "Ad Blitz", "details": "Aggressive Instagram ads for membership", "impact": "High"}
            ],
            "boutique": [
                {"name": "Zara Local", "action": "Seasonal Sale", "details": "End of season up to 50%", "impact": "Critical"},
                {"name": "FabIndia", "action": "New Collection", "details": "Summer Silks launched", "impact": "High"}
            ]
        }
        
        return rivals.get(business_niche.lower(), [
            {"name": "Generic Rival", "action": "Price Drop", "details": "Prices lowered by 10%", "impact": "Medium"}
        ])

competitor_service = CompetitorService()
