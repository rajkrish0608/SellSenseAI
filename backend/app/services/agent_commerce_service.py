import logging
from typing import Dict, Any
from app.services.negotiator_agent import agent_negotiator
from app.models.sql_models import BusinessProfile

logger = logging.getLogger(__name__)

class AgentCommerceService:
    """
    Simulates the bridge between the internet (external AI agents) 
    and the SellSenseai negotiation engine.
    """
    
    async def handle_agent_request(self, external_agent_json: Dict[str, Any], business_id: int, db: Any) -> Dict[str, Any]:
        """
        The entry point for an external AI (like Siri or a personal assistant bot)
        to 'talk' to the business.
        """
        business = db.query(BusinessProfile).filter(BusinessProfile.id == business_id).first()
        if not business:
            return {"error": "Business not found"}
            
        logger.info(f"🤖 [AGENTIC COMMERCE] External Request: {external_agent_json}")
        
        # In a real system, this would involve a multi-step LLM chain
        proposal = agent_negotiator.negotiate_deal(external_agent_json, business)
        
        logger.info(f"🤝 [AGENTIC COMMERCE] Negotiated Deal: {proposal['price']}")
        
        return proposal

agent_commerce_service = AgentCommerceService()
