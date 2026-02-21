import logging
import json
from typing import List, Dict, Any
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

class CompetitorAnalyzerAgent:
    """
    Agent to analyze competitor activities and suggest retaliation strategies.
    """
    
    def analyze_rival_move(self, business_profile: Any, rival_activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a competitor move and suggests a counter-campaign.
        """
        prompt = f"""
        You are the Head of Growth for {business_profile.business_name}.
        Niche: {business_profile.niche}
        
        A competitor has just made a move:
        Competitor: {rival_activity['name']}
        Action: {rival_activity['action']}
        Details: {rival_activity['details']}
        Impact: {rival_activity['impact']}
        
        Task: Analyze this move and suggest a "retaliation" strategy. 
        Your goal is to neutralize their advantage or steal their momentum.
        
        Return JSON ONLY:
        {{
            "strategy_name": "Name of counter-campaign",
            "analysis": "Brief analysis of why this counter-move works",
            "action_item": "E.g., Price drop, specific ad theme, flash sale",
            "whatsapp_alert": "The alert message to send to the business owner"
        }}
        """
        
        return gemini_service.generate_json(prompt)

competitor_analyzer = CompetitorAnalyzerAgent()
