import os
import httpx
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "sell_sense_ai_token")
        self.is_configured = bool(self.access_token and self.phone_number_id)
        
        if not self.is_configured:
            logger.warning("WhatsApp API keys not detected. Running in Local Mock Mode. Messages will be printed to console.")

    async def send_message(self, to_phone_number: str, text: str):
        """
        Sends a WhatsApp message using the Meta Cloud API.
        If no API keys are present, simply prints the message to the console for testing.
        """
        if not self.is_configured:
            # Local Mock Mode
            print(f"\n📱 [WHATSAPP MOCK - TO: {to_phone_number}]")
            print(f"{text}")
            print("-" * 40)
            return True

        url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "text",
            "text": {"body": text}
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                logger.info(f"WhatsApp message sent successfully to {to_phone_number}")
                return True
            except httpx.HTTPError as e:
                logger.error(f"Failed to send WhatsApp message: {str(e)}")
                return False

whatsapp_service = WhatsAppService()
