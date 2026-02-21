from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class CampaignBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = "draft"
    strategy_data: Optional[str] = None # JSON string
    insights_data: Optional[str] = None # JSON string

# Properties to receive on creation
class CampaignCreate(CampaignBase):
    name: str
    type: str

# Properties to receive on update
class CampaignUpdate(CampaignBase):
    pass

# Properties shared by models stored in DB
class CampaignInDBBase(CampaignBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class Campaign(CampaignInDBBase):
    pass

class CampaignInDB(CampaignInDBBase):
    pass
