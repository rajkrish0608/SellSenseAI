import logging
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.trend_service import trend_service
from app.services.trend_analyzer_agent import trend_analyzer_agent
from app.services.whatsapp_service import whatsapp_service
from app.models.sql_models import User, BusinessProfile

logger = logging.getLogger(__name__)

async def run_trend_jacking_cycle():
    """
    The main proactive loop.
    1. Fetches trends.
    2. Analyzes them for every active user.
    3. Sends WhatsApp alerts for high-relevance matches.
    """
    db = SessionLocal()
    try:
        # 1. Fetch current macro trends
        trends = trend_service.get_market_trends()
        
        # 2. Iterate through users who have phone numbers
        users = db.query(User).filter(User.phone != None).all()
        
        for user in users:
            business = user.business_profile
            if not business:
                continue
                
            # 3. Analyze relevance for this specific user
            scored_trends = await trend_analyzer_agent.analyze_relevance(business, trends)
            
            for scored in scored_trends:
                # Trigger WhatsApp if relevance is high (e.g. > 0.8)
                if scored.get("is_relevant") and scored.get("relevance_score", 0) >= 0.8:
                    hook_text = scored.get("proactive_hook", f"A new trend '{scored['name']}' is trending!")
                    logger.info(f"🚀 PROACTIVE ALERT for {user.phone}: {hook_text}")
                    
                    # Send actual WhatsApp (or Mock print)
                    await whatsapp_service.send_message(user.phone, hook_text)
                    
                    # For demo purposes, we only send one alert per cycle per user
                    break
                    
    except Exception as e:
        logger.error(f"Error in trend-jacking cycle: {e}")
    finally:
        db.close()

def start_trend_monitoring():
    """
    Start the background monitoring loop.
    """
    async def loop():
        while True:
            logger.info("Checking for new market trends...")
            await run_trend_jacking_cycle()
            # Wait 1 hour between cycles in production, 1 min for demo/test
            await asyncio.sleep(60) 
            
    # In a real FastAPI app, this would be registered as a lifespan event
    # For now, we provide this as a utility function.
    pass
