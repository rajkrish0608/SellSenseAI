from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.sql_models import Campaign, User
from app.schemas import campaign as campaign_schemas

router = APIRouter()

@router.get("", response_model=List[campaign_schemas.Campaign])
def read_campaigns(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve campaigns.
    """
    campaigns = (
        db.query(Campaign)
        .filter(Campaign.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return campaigns

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.services.campaign_orchestrator import run_campaign_workflow

# ... imports ...

@router.post("", response_model=campaign_schemas.Campaign)
def create_campaign(
    *,
    db: Session = Depends(deps.get_db),
    campaign_in: campaign_schemas.CampaignCreate,
    current_user: User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks
) -> Any:
    """
    Create new campaign.
    """
    campaign = Campaign(
        name=campaign_in.name,
        type=campaign_in.type,
        user_id=current_user.id,
        status="processing", 
        strategy_data="{}",
        insights_data="{}"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    # Trigger background workflow
    background_tasks.add_task(run_campaign_workflow, campaign.id, db)
    
    return campaign

@router.get("/active", response_model=Optional[campaign_schemas.Campaign])
def read_active_campaign(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the latest active/processing campaign.
    """
    campaign = (
        db.query(Campaign)
        .filter(Campaign.user_id == current_user.id)
        .order_by(Campaign.created_at.desc())
        .first()
    )
    return campaign

@router.put("/{id}", response_model=campaign_schemas.Campaign)
def update_campaign(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    campaign_in: campaign_schemas.CampaignUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a campaign.
    """
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    update_data = campaign_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
@router.get("/{id}", response_model=campaign_schemas.Campaign)
def read_campaign_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific campaign by ID.
    """
    campaign = db.query(Campaign).filter(Campaign.id == id, Campaign.user_id == current_user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/{id}/content", response_model=List[Any])
def read_campaign_content(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all content pieces (captions, video urls, etc) for a campaign.
    """
    from app.models.sql_models import CampaignContent
    content_pieces = (
        db.query(CampaignContent)
        .filter(CampaignContent.campaign_id == id)
        .order_by(CampaignContent.day_number.asc())
        .all()
    )
    return content_pieces
