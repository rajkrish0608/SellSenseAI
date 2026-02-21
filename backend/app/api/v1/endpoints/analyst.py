from typing import Any
import json

from fastapi import APIRouter, Depends, HTTPException

from app.api import deps
from app.services.gemini_service import gemini_service
from app.schemas.agents import AnalystRequest
from app.models.sql_models import User

router = APIRouter()

@router.post("/analyze")
def analyze_sales(
    request: AnalystRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Analyst Bot: Analyze sales data and provide insights
    """
    
    # Construct prompt
    sales_summary = json.dumps(request.sales_data.dict(), indent=2)
    business_info = f"{request.business_profile.business_name} ({request.business_profile.niche})"
    
    prompt = f"""You are an expert data analyst for small businesses.
    
    BUSINESS: {business_info}
    TARGET AUDIENCE: {request.business_profile.target_audience}
    
    SALES DATA:
    {sales_summary}
    
    TASK:
    Analyze this data to find trends, opportunities, and weaknesses.
    
    Return ONLY valid JSON:
    {{
      "summary": "Brief summary of performance (2 sentences)",
      "key_trends": ["Trend 1", "Trend 2", "Trend 3"],
      "top_performing_product": "Name of best product",
      "underperforming_product": "Name of worst product",
      "recommended_focus": {{
        "product": "Product to push next week",
        "reason": "Why this product?"
      }},
      "marketing_angle": "Suggested marketing angle based on data"
    }}"""
    
    insights = gemini_service.generate_json(prompt)
    
    if not insights:
        # Fallback if AI fails
        return {
            "summary": "Data analysis unavailable at the moment.",
            "key_trends": ["Sales patterns detected", "Customer activity stable"],
            "top_performing_product": "N/A",
            "underperforming_product": "N/A",
            "recommended_focus": {"product": "General Promotion", "reason": "AI unavailable"},
            "marketing_angle": "Focus on brand awareness"
        }
        
    return insights
