from fastapi import APIRouter
from app.api.v1.endpoints import auth, analyst, strategy, content, campaigns, whatsapp, trends

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(analyst.router, prefix="/analyst", tags=["analyst"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
