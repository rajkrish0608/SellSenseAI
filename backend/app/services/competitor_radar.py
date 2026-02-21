import logging
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.competitor_service import competitor_service
from app.services.competitor_analyzer_agent import competitor_analyzer
from app.services.whatsapp_service import whatsapp_service
from app.models.sql_models import User

logger = logging.getLogger(__name__)

async def run_competitor_radar_cycle():
    """
    The background loop for "God Mode" Phase 1: Competitor Radar.
    1. Scan rivals.
    2. Analyze moves.
    3. Alert the owner.
    """
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.phone != None).all()
        for user in users:
            business = user.business_profile
            if not business: continue
            
            # 1. Scan for rival activity
            activities = competitor_service.get_rival_activities(business.niche or "coffee")
            
            for activity in activities:
                # 2. Analyze move if "High" or "Critical" impact
                if activity["impact"] in ["High", "Critical"]:
                    analysis = competitor_analyzer.analyze_rival_move(business, activity)
                    
                    # 3. Alert the owner via WhatsApp
                    alert_msg = f"⚔️ *COMPETITOR RADAR ALERT* ⚔️\\n\\n{analysis.get('whatsapp_alert', 'A rival is making a move!')}\\n\\nStrategy: {analysis.get('strategy_name')}\\nReply 'RETALIATE' to launch the counter-campaign."
                    
                    logger.info(f"Pushing Competitor Radar alert to {user.phone}")
                    await whatsapp_service.send_message(user.phone, alert_msg)
                    
    except Exception as e:
        logger.error(f"Error in competitor radar cycle: {e}")
    finally:
        db.close()

async def start_competitor_radar():
    """Starts the endless loop."""
    while True:
        logger.info("Running Competitor Radar cycle...")
        await run_competitor_radar_cycle()
        await asyncio.sleep(300) # Every 5 mins for demo
