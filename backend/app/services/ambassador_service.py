import logging
import uuid
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AmbassadorService:
    """
    Manages the 'Digital Twins' or consistent characters for a brand.
    Handles reference images and consistency tokens (e.g., for LoRA or consistent character prompts).
    """
    
    def get_available_ambassadors(self) -> List[Dict[str, Any]]:
        """
        Returns a list of predefined AI personas that can represent a brand.
        """
        return [
            {
                "id": "persona_1",
                "name": "Sarah - Professional & Polished",
                "description": "Mid-30s, crisp professional attire, authoritative but friendly. Perfect for luxury or B2B.",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah",
                "consistency_token": "persona_sarah_polished_v1"
            },
            {
                "id": "persona_2",
                "name": "Leo - High Energy & Gen Z",
                "description": "Early 20s, streetwear, vibrant and enthusiastic. Perfect for cafes, apps, or fashion.",
                "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=leo",
                "consistency_token": "persona_leo_vibrant_v2"
            }
        ]

    def get_consistency_prompt_suffix(self, persona_id: str) -> str:
        """
        Returns a detailed visual prompt suffix to ensure the AI video generator
        keeps the character's face and style consistent.
        """
        ambassadors = {p["id"]: p for p in self.get_available_ambassadors()}
        persona = ambassadors.get(persona_id)
        if not persona: return ""
        
        return f" Featuring the brand ambassador {persona['name']}, maintaining strict facial consistency, same attire, and expressive high-definition cinematic lighting."

ambassador_service = AmbassadorService()
