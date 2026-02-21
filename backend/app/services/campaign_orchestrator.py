import json
import time
from sqlalchemy.orm import Session
from app.models.sql_models import Campaign, User, BusinessProfile
from app.services.gemini_service import gemini_service

async def run_campaign_workflow(campaign_id: int, db: Session):
    """
    Orchestrates the AI agents to generate a campaign.
    This is meant to be run as a background task.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        return

    try:
        # 1. Analyst Bot
        # In a real app, we'd fetch SalesUpdate data. For now, use mock data.
        mock_sales_data = {
            "total_revenue": 124500,
            "period": "Last Month",
            "top_product": "Premium Plan",
            "growth": 12.5
        }
        
        # Simulate processing time
        time.sleep(2) 
        
        user = db.query(User).filter(User.id == campaign.user_id).first()
        business_profile = user.business_profile
        
        analyst_prompt = f"""
        Analyze this sales data: {json.dumps(mock_sales_data)}
        For business: {business_profile.business_name} ({business_profile.niche})
        Target Audience: {business_profile.target_audience}
        """
        
        insights = gemini_service.generate_json(
            f"You are a Data Analyst. {analyst_prompt} Provide key insights and a recommended focus."
        )
        
        if insights:
            campaign.insights_data = json.dumps(insights)
            db.commit()
        
        # 2. Strategy Bot
        time.sleep(2)
        strategy_prompt = f"""
        Based on these insights: {json.dumps(insights)}
        Create a 7-day marketing strategy for {business_profile.business_name}.
        """
        
        strategy = gemini_service.generate_json(
            f"You are a Marketing Strategist. {strategy_prompt} Return a daily plan."
        )
        
        if strategy:
            campaign.strategy_data = json.dumps(strategy)
            db.commit()

        # 3. Content Bot
        time.sleep(2)
        from app.models.sql_models import CampaignContent
        from app.services.voice_service import voice_service
        from app.services.video_service import video_service

        daily_plan = strategy.get('daily_plan', [])
        for day in daily_plan[:3]: # Let's generate 3 days for the demo
            day_num = day.get('day')
            content_prompt = f"""
            Create content for Day {day_num} of this strategy.
            Theme: {day.get('theme')}
            
            Return JSON ONLY:
            {{
                "instagram_caption": "...",
                "whatsapp_message": "...",
                "poster_text": "...",
                "video_script": "...",
                "video_directing_prompt": "..."
            }}
            """
            
            content = gemini_service.generate_json(content_prompt)
            
            if content:
                # Generate AI Media
                audio_url = None
                if content.get("video_script"):
                    audio_url = await voice_service.generate_speech(content["video_script"], f"audio_{campaign_id}_{day_num}.mp3")
                
                video_url = None
                if content.get("video_directing_prompt"):
                    video_url = await video_service.generate_video(content["video_directing_prompt"])

                new_content = CampaignContent(
                    campaign_id=campaign_id,
                    day_number=day_num,
                    content_type="Social Post",
                    caption=content.get("instagram_caption"),
                    image_prompt=content.get("poster_text"),
                    video_url=video_url,
                    audio_url=audio_url,
                    is_posted=False
                )
                db.add(new_content)
        
        # Finally mark as completed
        campaign.status = "completed"
        db.commit()

    except Exception as e:
        print(f"Error in campaign workflow: {e}")
        campaign.status = "failed"
        db.commit()
