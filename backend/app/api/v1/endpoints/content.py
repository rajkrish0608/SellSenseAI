from typing import Any
import json

from fastapi import APIRouter, Depends

from app.api import deps
from app.services.gemini_service import gemini_service
from app.services.voice_service import voice_service
from app.services.video_service import video_service
from app.services.ambassador_service import ambassador_service
from app.schemas.agents import ContentRequest
from app.models.sql_models import User

router = APIRouter()

@router.post("/generate")
async def generate_content(
    request: ContentRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Content Bot: Generate social media content for the strategy
    """
    
    strategy_str = json.dumps(request.strategy, indent=2)
    
    daily_content = []
    daily_plan = request.strategy.get('daily_plan', [])
    
    # We'll batch generate or generate day by day. 
    # For speed in this demo, let's generate all at once or limits to 3 days if strict on time.
    # But usually day by day is better for quality.
    # Let's do Day 1 only for the "MVP" speed, OR loop through all.
    # The legacy code looped through all 7.
    
    for day in daily_plan[:7]:
        day_num = day.get('day')
        prompt = f"""Create content for Day {day_num}.
        Business: {request.business_profile.business_name}
        Theme: {day.get('theme')}
        Message: {day.get('key_message')}
        CTA: {day.get('call_to_action')}
        
        Return JSON:
        {{
            "instagram_caption": "Caption with hashtags",
            "whatsapp_message": "Short message",
            "poster_text": "Short text for image",
            "video_script": "A 15-second script for a TikTok/Reel narration",
            "video_directing_prompt": "Highly detailed visual description for an AI video generator (Luma/Runway)"
        }}"""
        
        content = gemini_service.generate_json(prompt, max_tokens=1000)
        
        if content:
            # Generate AI Voiceover
            voice_script = content.get("video_script", "")
            audio_url = None
            if voice_script:
                audio_url = await voice_service.generate_speech(voice_script, f"audio_day_{day_num}.mp3")

            # Generate AI Video
            video_prompt = content.get("video_directing_prompt", "")
            
            # Apply AI Ambassador Face Consistency (Phase 2 God Mode)
            # In a real app, we'd pull the user's selected persona from the DB
            persona_id = "persona_1" 
            consistency_suffix = ambassador_service.get_consistency_prompt_suffix(persona_id)
            if video_prompt and consistency_suffix:
                video_prompt += consistency_suffix

            video_url = None
            if video_prompt:
                video_url = await video_service.generate_video(video_prompt)

            daily_content.append({
                "day": day_num,
                "theme": day.get('theme'),
                "video_url": video_url,
                "audio_url": audio_url,
                **content
            })
            
    return {
        "daily_content": daily_content,
        "total_days": len(daily_content)
    }
