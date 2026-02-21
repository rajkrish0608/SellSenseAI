from fastapi import APIRouter, Request, Response, Depends, HTTPException, BackgroundTasks
import logging
import os
from sqlalchemy.orm import Session
from app.api import deps
from app.services.whatsapp_agent import whatsapp_agent

router = APIRouter()
logger = logging.getLogger(__name__)

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "sell_sense_ai_token")

@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Required by Meta (Facebook) to verify the webhook URL.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logger.info("WhatsApp WEBHOOK_VERIFIED")
            return Response(content=challenge, status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    
    raise HTTPException(status_code=400, detail="Missing parameters")

@router.post("/webhook")
async def receive_message(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    """
    Receives incoming text messages from users via WhatsApp.
    """
    data = await request.json()
    
    try:
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    
                    if messages:
                        message = messages[0]
                        # Only handle text messages for now
                        if message.get("type") == "text":
                            phone_number = message["from"]  # The sender's phone number
                            message_text = message["text"]["body"]  # The actual text

                            # Offload the processing to a background task so we return 200 to Meta immediately
                            # Meta requires a 200 OK within 3 seconds
                            # Note: For production, using Celery/Redis is preferred over FastAPI BackgroundTasks for stability
                            background_tasks.add_task(
                                process_whatsapp_message, 
                                phone_number, 
                                message_text, 
                            )
            return {"status": "success"}
    except Exception as e:
        logger.error(f"Error parsing WhatsApp webhook: {str(e)}")
        
    return {"status": "processed or ignored"}

async def process_whatsapp_message(phone_number: str, message_text: str):
    # Here we need a new DB session since we are in a background task
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        await whatsapp_agent.process_incoming_message(phone_number, message_text, db)
    finally:
        db.close()
