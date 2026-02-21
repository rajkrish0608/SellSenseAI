import logging
import json
from typing import List, Dict, Any, Optional
from app.services.gemini_service import gemini_service
from app.models.sql_models import AdCampaign, AdPerformance

logger = logging.getLogger(__name__)

class AdOptAgent:
    """
    Agent that analyzes ad performance and makes budget optimization decisions.
    Implements A/B testing logic.
    """
    
    async def analyze_and_optimize(self, ad_campaign: AdCampaign, performance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Uses Gemini to decide if we should scale, pause, or pivot an ad campaign.
        """
        prompt = f"""
        You are a Media Buying Specialist for SellSenseai.
        
        Ad Campaign: {ad_campaign.id}
        Platform: {ad_campaign.platform}
        Current Budget: ${ad_campaign.budget}
        
        Real-time Performance Metrics:
        {json.dumps(performance_data, indent=2)}
        
        Task: Analyze the data. If CTR (Click-Through Rate) is below 1%, recommend pausing. 
        If it's an A/B test (multiple creatives), select the winner and move full budget there.
        
        Return JSON ONLY:
        {{
            "decision": "scale" | "pause" | "reallocate" | "hold",
            "reasoning": "Quick explanation",
            "suggested_budget_adjustment": 0.0,
            "winner_ad_id": "if applicable"
        }}
        """
        
        decision = gemini_service.generate_json(prompt)
        return decision

ad_opt_agent = AdOptAgent()
