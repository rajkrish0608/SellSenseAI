import logging
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.ad_service import ad_service
from app.services.ad_opt_agent import ad_opt_agent
from app.models.sql_models import AdCampaign, AdPerformance

logger = logging.getLogger(__name__)

async def run_ad_optimization_cycle():
    """
    The background loop for managing ads.
    1. Fetches real metrics from the platform.
    2. Uses AI to decide on optimization.
    3. Updates budgets or pauses ads.
    """
    db = SessionLocal()
    try:
        active_ads = db.query(AdCampaign).filter(AdCampaign.status == 'active').all()
        
        for ad in active_ads:
            # 1. Fetch current metrics
            metrics = await ad_service.get_ad_metrics(ad.ad_id)
            
            # 2. Store metrics in DB for history
            perf = AdPerformance(
                ad_campaign_id=ad.id,
                clicks=metrics["clicks"],
                impressions=metrics["impressions"],
                ctr=metrics["ctr"],
                spend=metrics["spend"]
            )
            db.add(perf)
            db.commit()
            
            # 3. Optimize using AI
            if ad.auto_pilot:
                optimization = await ad_opt_agent.analyze_and_optimize(ad, [metrics])
                decision = optimization.get("decision")
                reason = optimization.get("reasoning")
                
                logger.info(f"AI Ad Decision for {ad.id}: {decision} ({reason})")
                
                if decision == "pause":
                    ad.status = "paused"
                    db.commit()
                    logger.info(f"Paused Ad {ad.id} due to low performance.")
                elif decision == "scale":
                    ad.budget += optimization.get("suggested_budget_adjustment", 0)
                    db.commit()
                    logger.info(f"Scaled budget for Ad {ad.id}.")
                    
    except Exception as e:
        logger.error(f"Error in ad optimization cycle: {e}")
    finally:
        db.close()

def start_ad_management():
    """
    Start the background ad management loop.
    """
    async def loop():
        while True:
            logger.info("Running Ad Optimization cycle...")
            await run_ad_optimization_cycle()
            # Wait 24 hours in production, 1 min for demo
            await asyncio.sleep(60) 
    pass
