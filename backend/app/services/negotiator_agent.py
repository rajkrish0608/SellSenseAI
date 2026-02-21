import logging
import json
from typing import Any, Dict
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

class AgentNegotiatorAgent:
    """
    The AI 'Sales Closer' designed to talk to other AI agents.
    Handles pricing negotiation, stock availability, and discount approvals.
    """
    
    def negotiate_deal(self, request_from_agent: Dict[str, Any], business_profile: Any) -> Dict[str, Any]:
        """
        Parses a request from an external AI agent (e.g., 'Find me coffee under $15')
        and returns a structured proposal or counter-offer.
        """
        prompt = f"""
        You are the Sales Negotiator Agent for {business_profile.business_name}.
        Brand Vibe: {business_profile.niche}
        
        Incoming Request from an External AI Assistant:
        {json.dumps(request_from_agent)}
        
        Task: Negotiate the best deal for the business while converted the lead.
        You have authority to offer up to 15% discount for first-time AI-driven orders.
        
        Return JSON-LD (Schema.org compliant where possible):
        {{
            "@context": "https://schema.org",
            "@type": "Offer",
            "itemOffered": {{
                "@type": "Product",
                "name": "Product name matching the request",
                "description": "Short, agent-parseable description"
            }},
            "price": "Final negotiated price",
            "priceCurrency": "INR",
            "negotiation_logic": "Why you chose this price/discount",
            "status": "Accepted" | "Counter-Offer" | "Declined"
        }}
        """
        
        return gemini_service.generate_json(prompt)

agent_negotiator = AgentNegotiatorAgent()
