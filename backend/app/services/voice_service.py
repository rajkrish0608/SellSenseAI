import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Default character
        self.is_configured = bool(self.api_key)

        if not self.is_configured:
            logger.warning("ElevenLabs API key not found. Running VoiceService in Mock Mode.")

    async def generate_speech(self, text: str, output_path: str) -> Optional[str]:
        """
        Converts text to speech using ElevenLabs API.
        Returns the path to the saved audio file.
        """
        if not self.is_configured:
            logger.info(f"Mocking Voice Generation for: {text[:50]}...")
            # In a real mock, we could return a placeholder audio file
            return "mock_audio_url_placeholder.mp3"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                return output_path
            except Exception as e:
                logger.error(f"ElevenLabs error: {e}")
                return None

voice_service = VoiceService()
