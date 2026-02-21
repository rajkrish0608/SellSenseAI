import google.generativeai as genai
import json
import logging
from typing import Any, Dict, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.GOOGLE_GEMINI_API_KEY:
            logger.warning("⚠️ Google Gemini API key not found in settings!")
            self.model = None
            return

        genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
        # Using 1.5 Flash as per legacy code recommendation for speed/cost
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Google Gemini AI initialized!")

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        if not self.model:
            logger.error("Gemini model not initialized")
            return None

        try:
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            logger.error(f"❌ Gemini error: {e}")
            return None

    def generate_json(self, prompt: str, max_tokens: int = 3000) -> Optional[Dict[str, Any]]:
        if not self.model:
            return None

        try:
            full_prompt = f"""{prompt}

CRITICAL: Return ONLY valid JSON. No markdown, no explanations, no text before or after JSON.
Start directly with {{ and end with }}"""

            response_text = self.generate(full_prompt, temperature=0.3, max_tokens=max_tokens)
            if not response_text:
                return None

            cleaned = response_text.strip()
            # Remove markdown code blocks if present
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()

            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parse error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return None

# Singleton instance
gemini_service = GeminiService()
