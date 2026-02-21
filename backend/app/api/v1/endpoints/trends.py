from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.services.trend_service import trend_service

router = APIRouter()

@router.get("", response_model=List[Any])
def get_trends(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current market trends.
    """
    return trend_service.get_market_trends()
