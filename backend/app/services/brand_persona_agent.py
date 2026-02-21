import logging
import json
from typing import Any, Dict
from app.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

class BrandPersonaAgent:
    """
    Defines the brand voice, visual aesthetics, and persona 'soul' 
    to ensure all AI-generated content feels unified.
    """
    
    def define_brand_vibe(self, business_profile: Any) -> Dict[str, Any]:
        """
        Uses Gemini to define a unique brand persona based on the business profile.
        """
        prompt = f"""
        Business Name: {business_profile.business_name}
        Niche: {business_profile.niche}
        Description: {business_profile.description}
        
        Task: Define a 'Digital Ambassador' persona for this brand. 
        Think about tone, visual style, and the dominant personality trait.
        
        Return JSON ONLY:
        {{
            "persona_name": "E.g. The Modern Artisan",
            "tone": "E.g. Minimalist, Warm, Playful",
            "visual_identity": "E.g. Soft pastels, cinematic closeups, organic textures",
            "voice_personality": "E.g. A calm, sophisticated voice with a slight British accent",
            "ideal_ambassador_id": "persona_1" | "persona_2"
        }}
        """
        
        return gemini_service.generate_json(prompt)

brand_persona_agent = BrandPersonaAgent()
