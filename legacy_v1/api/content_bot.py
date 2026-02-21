from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_services.gemini_ai import create_gemini_ai
from ai_services.simple_image_gen import create_simple_image_generator

content_bp = Blueprint('content', __name__)


@content_bp.route('/api/content/generate', methods=['POST'])
def generate_content():
    """
    🎨 CONTENT BOT
    
    Receives:
    - business_profile: {business_name, niche, target_audience, brand_voice}
    - strategy: object (from Strategy Bot)
    - insights: object (from Analyst Bot) - optional
    
    Returns:
    - daily_content: array of 7 days with:
      - instagram_caption
      - whatsapp_message
      - poster_text
      - poster_url
    """
    
    data = request.get_json()
    
    business_profile = data.get('business_profile', {})
    strategy = data.get('strategy', {})
    insights = data.get('insights', {})
    
    print("\n" + "="*70)
    print("🎨 CONTENT BOT - GENERATING DAILY CONTENT")
    print("="*70)
    print(f"Business: {business_profile.get('business_name', 'Unknown')}")
    print(f"Campaign: {strategy.get('campaign_name', 'N/A')}")
    print(f"Days to Generate: {len(strategy.get('daily_plan', []))}")
    
    # Initialize Google Gemini
    try:
        gemini = create_gemini_ai()
        print("✅ Google Gemini initialized")
    except Exception as e:
        print(f"❌ Failed to initialize AI: {e}")
        return jsonify({
            "status": "error",
            "message": f"Failed to initialize AI: {str(e)}"
        }), 500
    
    daily_content = []
    
    # Generate content for each day
    for day_plan in strategy.get('daily_plan', [])[:7]:
        day_num = day_plan.get('day', 0)
        print(f"   📝 Generating Day {day_num} content...")
        
        # Create content prompt
        prompt = f"""You are a creative social media content creator for small businesses.

BUSINESS INFORMATION:
- Business Name: {business_profile.get('business_name', 'Business')}
- Niche: {business_profile.get('niche', 'General')}
- Brand Voice: {business_profile.get('brand_voice', 'Friendly')}
- Target Audience: {business_profile.get('target_audience', 'General customers')}

DAY {day_num} CAMPAIGN PLAN:
- Theme: {day_plan.get('theme', 'N/A')}
- Objective: {day_plan.get('objective', 'N/A')}
- Key Message: {day_plan.get('key_message', 'N/A')}
- Tone: {day_plan.get('tone', 'friendly')}
- Call-to-Action: {day_plan.get('call_to_action', 'Shop now')}

FOCUS PRODUCT (if applicable):
{insights.get('recommended_focus', {}).get('product', 'Your products')}

TASK:
Create engaging social media content for this day.

Return ONLY valid JSON:
{{
  "instagram_caption": "Full Instagram caption with emojis, engaging copy, and 5-7 hashtags",
  "whatsapp_message": "Short WhatsApp broadcast message (2-3 sentences, friendly tone)",
  "poster_text": "Short catchy text for poster (5-7 words maximum)"
}}"""
        
        # Generate content
        content = gemini.generate_json(prompt, max_tokens=1500)
        
        if content:
            daily_content.append({
                "day": day_num,
                "theme": day_plan.get('theme', f'Day {day_num}'),
                "instagram_caption": content.get('instagram_caption', ''),
                "instagram_hashtags": extract_hashtags(content.get('instagram_caption', '')),
                "whatsapp_message": content.get('whatsapp_message', ''),
                "poster_text": content.get('poster_text', day_plan.get('theme', ''))
            })
            print(f"      ✅ Day {day_num} content generated")
        else:
            # Fallback content
            print(f"      ⚠️  Day {day_num} using fallback content")
            daily_content.append({
                "day": day_num,
                "theme": day_plan.get('theme', f'Day {day_num}'),
                "instagram_caption": generate_fallback_caption(day_plan, business_profile),
                "instagram_hashtags": ["sale", "shopping", "deals", "new", "trending"],
                "whatsapp_message": f"{day_plan.get('key_message', 'Special offer!')} {day_plan.get('call_to_action', 'Shop now!')} 🛍️",
                "poster_text": day_plan.get('theme', f'Day {day_num}')
            })
    
    # Generate AI posters
    print("\n   🖼️  Generating AI posters...")
    try:
        img_gen = create_simple_image_generator()
        themes = ['default', 'blue', 'purple', 'green', 'dark']
        
        for i, content in enumerate(daily_content[:5]):  # First 5 days
            theme = themes[i % len(themes)]
            poster_path = img_gen.generate_poster(
                content['poster_text'],
                theme=theme
            )
            
            if poster_path:
                content['poster_url'] = f"/{poster_path}"
                print(f"      ✅ Poster {i+1} created ({theme} theme)")
            else:
                content['poster_url'] = None
                print(f"      ⚠️  Poster {i+1} generation skipped")
    
    except Exception as e:
        print(f"      ⚠️  Poster generation skipped: {e}")
        for content in daily_content:
            content['poster_url'] = None
    
    print(f"\n✅ CONTENT GENERATION COMPLETE!")
    print(f"   Total Days: {len(daily_content)}")
    print(f"   Posters Created: {sum(1 for c in daily_content if c.get('poster_url'))}")
    print("="*70 + "\n")
    
    return jsonify({
        "daily_content": daily_content,
        "total_days": len(daily_content)
    }), 200


def extract_hashtags(caption):
    """Extract hashtags from caption"""
    words = caption.split()
    hashtags = [word.strip('#') for word in words if word.startswith('#')]
    return hashtags[:7]


def generate_fallback_caption(day_plan, business_profile):
    """Generate fallback caption if AI fails"""
    emojis = ['✨', '🌟', '💫', '🎉', '🎊', '🛍️', '💝']
    
    caption = f"{emojis[0]} {day_plan.get('theme', 'Special Day')} {emojis[1]}\n\n"
    caption += f"{day_plan.get('key_message', 'Check out our amazing products!')} "
    caption += f"{emojis[2]}\n\n"
    caption += f"{day_plan.get('call_to_action', 'Shop now!')} "
    caption += f"{emojis[3]}\n\n"
    caption += "#sale #shopping #deals #new #trending #offer #special"
    
    return caption


@content_bp.route('/api/content/health', methods=['GET'])
def content_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "content",
        "message": "Content Bot is ready"
    }), 200