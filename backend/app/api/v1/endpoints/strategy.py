from typing import Any
import json

from fastapi import APIRouter, Depends

from app.api import deps
from app.services.gemini_service import gemini_service
from app.schemas.agents import StrategyRequest
from app.models.sql_models import User

router = APIRouter()

@router.post("/create")
def create_strategy(
    request: StrategyRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Strategy Bot: Create a 7-day marketing campaign strategy
    """
    
    insights_str = json.dumps(request.insights, indent=2)
    
    prompt = f"""You are an expert marketing strategist.

    BUSINESS: {request.business_profile.business_name}
    NICHE: {request.business_profile.niche}
    GOAL: {request.campaign_goal}
    
    INSIGHTS:
    {insights_str}
    
    TASK:
    Create a 7-day marketing plan.
    
    Return ONLY valid JSON:
    {{
      "campaign_name": "Catchy Name",
      "campaign_type": "Type (Flash Sale, Launch, etc)",
      "primary_objective": "Goal description",
      "key_message": "Core message",
      "daily_plan": [
        {{
          "day": 1,
          "theme": "Day Theme",
          "objective": "Day Objective",
          "key_message": "Day Message",
          "tone": "Tone",
          "call_to_action": "CTA"
        }},
        ... (for 7 days)
      ]
    }}"""
    
    strategy = gemini_service.generate_json(prompt, max_tokens=3500)
    
    if not strategy:
        # Simple Fallback
        return {
            "campaign_name": "Weekly Growth Campaign",
            "campaign_type": "Engagement",
            "daily_plan": []
        }
        
    return strategy
