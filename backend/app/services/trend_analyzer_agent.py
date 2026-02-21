import logging
import json
from typing import List, Dict, Any
from app.services.gemini_service import gemini_service
from app.models.sql_models import BusinessProfile

logger = logging.getLogger(__name__)

class TrendAnalyzerAgent:
    """
    Agent that analyzes market trends against a specific business profile.
    Calculates relevance scores and generates proactive notification text.
    """
    
    async def analyze_relevance(self, business: BusinessProfile, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Uses Gemini to score trends based on their marketing potential for the specific business.
        """
        prompt = f"""
        You are a Trend-Jacking Analyst for "{business.business_name}".
        Niche: {business.niche}
        Target Audience: {business.target_audience}
        
        Analyze these current market trends and decide if we should use them in a campaign.
        
        Trends:
        {json.dumps(trends, indent=2)}
        
        Return JSON ONLY for each trend with:
        {{
            "name": "Trend Name",
            "is_relevant": true | false,
            "relevance_score": 0.0 to 1.0,
            "proactive_hook": "A short WhatsApp text inviting the owner to act on this trend (e.g. 'Hey! [Trend] is viral. Should I turn it into a reel?')"
        }}
        """
        
        analysis = gemini_service.generate_json(prompt)
        # If Gemini returns a list or a dict containing a list of objects
        if isinstance(analysis, list):
            return analysis
        if isinstance(analysis, dict) and 'trends' in analysis:
            return analysis['trends']
        
        return []

trend_analyzer_agent = TrendAnalyzerAgent()
