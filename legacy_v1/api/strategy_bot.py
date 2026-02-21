from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_services.gemini_ai import create_gemini_ai

strategy_bp = Blueprint('strategy', __name__)


@strategy_bp.route('/api/strategy/create', methods=['POST'])
def create_strategy():
    """
    🧠 STRATEGY BOT
    
    Receives:
    - business_profile: {business_name, niche, target_audience, brand_voice}
    - campaign_goal: string (sales, awareness, engagement, etc.)
    - insights: object (from Analyst Bot)
    
    Returns:
    - campaign_name
    - campaign_type
    - primary_objective
    - key_message
    - daily_plan (7 days)
    """
    
    data = request.get_json()
    
    business_profile = data.get('business_profile', {})
    campaign_goal = data.get('campaign_goal', 'sales')
    insights = data.get('insights', {})
    
    print("\n" + "="*70)
    print("🧠 STRATEGY BOT - CREATING CAMPAIGN STRATEGY")
    print("="*70)
    print(f"Business: {business_profile.get('business_name', 'Unknown')}")
    print(f"Campaign Goal: {campaign_goal}")
    print(f"Has Insights: {bool(insights)}")
    
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
    
    # Create strategy prompt
    prompt = f"""You are an expert marketing strategist specializing in social media campaigns for small businesses.

BUSINESS PROFILE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Business Name: {business_profile.get('business_name', 'Business')}
- Niche/Industry: {business_profile.get('niche', 'General retail')}
- Target Audience: {business_profile.get('target_audience', 'General customers')}
- Brand Voice: {business_profile.get('brand_voice', 'Friendly')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAMPAIGN GOAL: {campaign_goal.upper()}

ANALYST INSIGHTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{json.dumps(insights, indent=2)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK:
Create a strategic 7-day Instagram/WhatsApp marketing campaign plan.

REQUIREMENTS:
- Create a narrative arc that builds momentum across 7 days
- Day 1-2: Introduction and awareness building
- Day 3-4: Engagement and social proof
- Day 5-6: Conversion and sales push
- Day 7: Final urgency and closing

Return ONLY valid JSON in this exact structure:
{{
  "campaign_name": "Creative, catchy campaign name (3-5 words)",
  "campaign_type": "flash_sale/product_launch/engagement_boost/brand_awareness/seasonal",
  "primary_objective": "Clear statement of the main campaign goal",
  "key_message": "Core message to communicate throughout the campaign",
  "daily_plan": [
    {{
      "day": 1,
      "theme": "Engaging theme for day 1",
      "objective": "Specific objective for this day",
      "key_message": "Main message to communicate on day 1",
      "tone": "exciting/friendly/urgent/inspirational/professional",
      "call_to_action": "Clear, actionable CTA for day 1"
    }},
    {{
      "day": 2,
      "theme": "Day 2 theme",
      "objective": "Day 2 objective",
      "key_message": "Day 2 message",
      "tone": "friendly/professional/exciting",
      "call_to_action": "Day 2 CTA"
    }},
    {{
      "day": 3,
      "theme": "Day 3 theme",
      "objective": "Day 3 objective",
      "key_message": "Day 3 message",
      "tone": "inspirational/exciting",
      "call_to_action": "Day 3 CTA"
    }},
    {{
      "day": 4,
      "theme": "Day 4 theme",
      "objective": "Day 4 objective",
      "key_message": "Day 4 message",
      "tone": "friendly/exciting",
      "call_to_action": "Day 4 CTA"
    }},
    {{
      "day": 5,
      "theme": "Day 5 theme",
      "objective": "Day 5 objective",
      "key_message": "Day 5 message",
      "tone": "urgent/exciting",
      "call_to_action": "Day 5 CTA"
    }},
    {{
      "day": 6,
      "theme": "Day 6 theme",
      "objective": "Day 6 objective",
      "key_message": "Day 6 message",
      "tone": "urgent/exciting",
      "call_to_action": "Day 6 CTA"
    }},
    {{
      "day": 7,
      "theme": "Final Push - Last Chance",
      "objective": "Close maximum sales",
      "key_message": "Last chance message with strong urgency",
      "tone": "urgent",
      "call_to_action": "Last chance CTA - act now!"
    }}
  ]
}}"""
    
    print("📋 Planning 7-day campaign strategy with Google Gemini...")
    
    # Generate strategy using Gemini
    strategy = gemini.generate_json(prompt, max_tokens=3500)
    
    if not strategy:
        print("⚠️  AI generation failed, using fallback strategy")
        strategy = get_fallback_strategy()
    else:
        print("✅ Strategy generated successfully")
    
    # Log results
    print(f"\n🎯 STRATEGY RESULTS:")
    print(f"   Campaign Name: {strategy.get('campaign_name', 'N/A')}")
    print(f"   Campaign Type: {strategy.get('campaign_type', 'N/A')}")
    print(f"   Days Planned: {len(strategy.get('daily_plan', []))}")
    print("="*70 + "\n")
    
    return jsonify(strategy), 200


def get_fallback_strategy():
    """Fallback strategy if AI fails"""
    
    day_themes = [
        ("Grand Introduction", "Introduce the campaign", "We have something special for you!"),
        ("Product Spotlight", "Showcase key products", "Discover our amazing collection"),
        ("Customer Stories", "Build social proof", "See what our customers love"),
        ("Special Offer Reveal", "Create value perception", "Exclusive deals just for you"),
        ("Limited Availability", "Create urgency", "Limited stock - don't miss out"),
        ("Last 48 Hours", "Increase urgency", "Only 2 days left!"),
        ("Final Call", "Final conversion push", "Last chance - ends tonight!")
    ]
    
    return {
        "campaign_name": "7-Day Power Campaign",
        "campaign_type": "flash_sale",
        "primary_objective": "Drive sales and engagement through strategic 7-day content plan",
        "key_message": "Amazing products at unbeatable value - limited time only",
        "daily_plan": [
            {
                "day": i + 1,
                "theme": theme,
                "objective": objective,
                "key_message": message,
                "tone": "friendly" if i < 4 else "urgent",
                "call_to_action": "Shop Now!" if i < 5 else "Last Chance - Shop Now!"
            }
            for i, (theme, objective, message) in enumerate(day_themes)
        ]
    }


@strategy_bp.route('/api/strategy/health', methods=['GET'])
def strategy_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "strategy",
        "message": "Strategy Bot is ready"
    }), 200