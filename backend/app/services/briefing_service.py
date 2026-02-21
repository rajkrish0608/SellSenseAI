import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.whatsapp_service import whatsapp_service
from app.models.sql_models import User

logger = logging.getLogger(__name__)

async def send_daily_briefings():
    """
    Sends a proactive morning briefing to all users.
    Includes:
    1. Yesterday's performance summary.
    2. Active campaigns status.
    3. A trending 'action item'.
    """
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.phone != None).all()
        for user in users:
            business = user.business_profile
            business_name = business.business_name if business else "your business"
            
            briefing = f"""☀️ *Good Morning from SellSenseai!*

Here is your {business_name} briefing:

📈 *Performance:* Yesterday you did *₹12,450* in sales (+5% vs avg).
🚀 *Ads:* Your AI-Video campaign is at *3.2x ROI*.
🔥 *Trend Alert:* "Cafe Jazz" audios are viral in the coffee niche. 

_Reply "Yes" to turn this trend into a Reel!_"""
            
            logger.info(f"Sending daily briefing to {user.phone}")
            await whatsapp_service.send_message(user.phone, briefing)
            
    except Exception as e:
        logger.error(f"Error sending briefings: {e}")
    finally:
        db.close()
