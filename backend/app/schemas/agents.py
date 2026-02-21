from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class BusinessProfile(BaseModel):
    business_name: str
    niche: Optional[str] = "General"
    target_audience: Optional[str] = "General"
    brand_voice: Optional[str] = "Friendly"

class SalesData(BaseModel):
    top_products: List[Dict[str, Any]] = []
    daily_revenue: List[Dict[str, Any]] = []
    
class AnalystRequest(BaseModel):
    business_profile: BusinessProfile
    sales_data: SalesData

class StrategyRequest(BaseModel):
    business_profile: BusinessProfile
    campaign_goal: str = "sales"
    insights: Dict[str, Any]

class ContentRequest(BaseModel):
    business_profile: BusinessProfile
    strategy: Dict[str, Any]
    insights: Optional[Dict[str, Any]] = {}

# Response Models
class DailyContent(BaseModel):
    day: int
    theme: str
    instagram_caption: str
    whatsapp_message: str
    poster_text: str
    video_script: Optional[str] = None
    video_directing_prompt: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    poster_url: Optional[str] = None
