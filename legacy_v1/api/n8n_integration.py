from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os
import json as json_module

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.models import db, Campaign, CampaignContent
from ai_services.gemini_ai import create_gemini_ai
from ai_services.simple_image_gen import create_simple_image_generator

n8n_bp = Blueprint('n8n', __name__)


@n8n_bp.route('/api/campaign/generate', methods=['POST'])
@login_required
def generate_campaign():
    """
    Generate complete campaign using 3 AI agents
    This runs all 3 bots sequentially: Analyst → Strategy → Content
    """
    
    data = request.get_json()
    campaign_goal = data.get('campaign_goal', 'sales')
    
    print("\n" + "="*70)
    print("🚀 STARTING CAMPAIGN GENERATION (Google Gemini)")
    print("="*70)
    
    # Get user business profile
    profile = current_user.business_profile
    
    if not profile:
        return jsonify({
            "status": "error",
            "message": "Please complete your business profile first"
        }), 400
    
    # Get sales data
    from database.models import SalesUpdate
    sales_data = SalesUpdate.query.filter_by(
        user_id=current_user.id
    ).order_by(SalesUpdate.week_start_date.desc()).limit(4).all()
    
    sales_list = [
        {
            "week": sale.week_start_date.isoformat(),
            "revenue": sale.total_revenue,
            "items_sold": sale.total_items_sold,
            "products": json_module.loads(sale.products_sold) if sale.products_sold else []
        } for sale in sales_data
    ]
    
    # Initialize AI
    try:
        gemini = create_gemini_ai()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to initialize AI: {str(e)}"
        }), 500
    
    # =====================================
    # STEP 1: ANALYST BOT
    # =====================================
    print("\n🔍 STEP 1: Running Analyst Bot...")
    
    analyst_prompt = f"""You are a business analyst. Analyze this sales data:

BUSINESS: {profile.business_name}
NICHE: {profile.niche or 'General'}

SALES DATA:
{json_module.dumps(sales_list, indent=2)}

Return ONLY JSON:
{{
  "best_selling_product": {{"name": "...", "total_revenue": 0}},
  "revenue_trend": {{"trend": "up/down/stable", "change_percent": 0}},
  "customer_insights": ["...", "..."],
  "opportunities": ["...", "..."],
  "recommended_focus": {{"product": "...", "reason": "..."}}
}}"""
    
    insights = gemini.generate_json(analyst_prompt, max_tokens=2000)
    
    if not insights:
        insights = {
            "best_selling_product": {"name": "Your products", "total_revenue": 0},
            "revenue_trend": {"trend": "stable", "change_percent": 0},
            "customer_insights": ["Focus on consistent posting"],
            "opportunities": ["Post at peak times"],
            "recommended_focus": {"product": "Best sellers", "reason": "Proven demand"}
        }
    
    print(f"✅ Analyst Bot complete! Focus: {insights.get('recommended_focus', {}).get('product')}")
    
    # =====================================
    # STEP 2: STRATEGIC BOT
    # =====================================
    print("\n🧠 STEP 2: Running Strategic Bot...")
    
    strategy_prompt = f"""You are a marketing strategist.

BUSINESS: {profile.business_name}
GOAL: {campaign_goal}

INSIGHTS:
{json_module.dumps(insights, indent=2)}

Create a 7-day campaign. Return ONLY JSON:
{{
  "campaign_name": "...",
  "campaign_type": "flash_sale/product_launch/engagement",
  "primary_objective": "...",
  "daily_plan": [
    {{"day": 1, "theme": "...", "objective": "...", "key_message": "...", "tone": "exciting", "call_to_action": "..."}},
    {{"day": 2, "theme": "...", "objective": "...", "key_message": "...", "tone": "friendly", "call_to_action": "..."}},
    {{"day": 3, "theme": "...", "objective": "...", "key_message": "...", "tone": "exciting", "call_to_action": "..."}},
    {{"day": 4, "theme": "...", "objective": "...", "key_message": "...", "tone": "friendly", "call_to_action": "..."}},
    {{"day": 5, "theme": "...", "objective": "...", "key_message": "...", "tone": "urgent", "call_to_action": "..."}},
    {{"day": 6, "theme": "...", "objective": "...", "key_message": "...", "tone": "urgent", "call_to_action": "..."}},
    {{"day": 7, "theme": "Final Push", "objective": "Close sales", "key_message": "...", "tone": "urgent", "call_to_action": "Last chance!"}}
  ]
}}"""
    
    strategy = gemini.generate_json(strategy_prompt, max_tokens=3000)
    
    if not strategy:
        strategy = {
            "campaign_name": "7-Day Campaign",
            "campaign_type": "flash_sale",
            "primary_objective": "Drive sales",
            "daily_plan": [
                {"day": i, "theme": f"Day {i}", "objective": "Engage", "key_message": "Shop now", "tone": "friendly", "call_to_action": "Shop!"}
                for i in range(1, 8)
            ]
        }
    
    print(f"✅ Strategic Bot complete! Campaign: {strategy.get('campaign_name')}")
    
    # =====================================
    # STEP 3: CONTENT BOT
    # =====================================
    print("\n🎨 STEP 3: Running Content Bot (7 days)...")
    
    daily_content = []
    
    for day_plan in strategy.get('daily_plan', [])[:7]:
        day_num = day_plan.get('day', 0)
        print(f"   Generating content for Day {day_num}...")
        
        content_prompt = f"""Create social media content:

BUSINESS: {profile.business_name}
DAY {day_num}: {day_plan.get('theme')}
MESSAGE: {day_plan.get('key_message')}
TONE: {day_plan.get('tone')}

Return ONLY JSON:
{{
  "instagram_caption": "Caption with emojis and hashtags",
  "whatsapp_message": "Short message (2-3 sentences)",
  "poster_text": "5-7 words for poster"
}}"""
        
        content = gemini.generate_json(content_prompt, max_tokens=1500)
        
        if content:
            daily_content.append({
                "day": day_num,
                "theme": day_plan.get('theme'),
                "instagram_caption": content.get('instagram_caption', ''),
                "whatsapp_message": content.get('whatsapp_message', ''),
                "poster_text": content.get('poster_text', day_plan.get('theme'))
            })
        else:
            daily_content.append({
                "day": day_num,
                "theme": day_plan.get('theme'),
                "instagram_caption": f"{day_plan.get('key_message')} {day_plan.get('call_to_action')} ✨ #sale #shopping",
                "whatsapp_message": f"{day_plan.get('key_message')} {day_plan.get('call_to_action')}",
                "poster_text": day_plan.get('theme')
            })
    
    print(f"✅ Content Bot complete! Generated {len(daily_content)} days of content")
    
    # =====================================
    # STEP 4: GENERATE POSTERS
    # =====================================
    print("\n🖼️  STEP 4: Generating posters...")
    
    try:
        img_gen = create_simple_image_generator()
        themes = ['default', 'blue', 'purple', 'green', 'dark']
        
        for i, content in enumerate(daily_content[:5]):
            poster_path = img_gen.generate_poster(
                content['poster_text'],
                theme=themes[i % len(themes)]
            )
            if poster_path:
                content['poster_url'] = f"/{poster_path}"
                print(f"   ✅ Poster {i+1} created")
            else:
                content['poster_url'] = None
    except Exception as e:
        print(f"   ⚠️  Poster generation skipped: {e}")
        for content in daily_content:
            content['poster_url'] = None
    
    # =====================================
    # STEP 5: SAVE TO DATABASE
    # =====================================
    print("\n💾 STEP 5: Saving to database...")
    
    try:
        campaign = Campaign(
            user_id=current_user.id,
            campaign_name=strategy.get('campaign_name', 'AI Generated Campaign'),
            campaign_type=strategy.get('campaign_type', 'general'),
            duration_days=7,
            strategy=json_module.dumps(strategy),
            insights=json_module.dumps(insights),
            status='active'
        )
        
        db.session.add(campaign)
        db.session.flush()
        
        for content_item in daily_content:
            content = CampaignContent(
                campaign_id=campaign.id,
                day_number=content_item.get('day'),
                content_type='instagram_post',
                caption=content_item.get('instagram_caption'),
                whatsapp_message=content_item.get('whatsapp_message'),
                theme=content_item.get('theme')
            )
            db.session.add(content)
        
        db.session.commit()
        
        print(f"✅ Campaign saved! ID: {campaign.id}")
        
    except Exception as e:
        print(f"❌ Error saving: {e}")
        db.session.rollback()
    
    print("\n" + "="*70)
    print("✅ CAMPAIGN GENERATION COMPLETE!")
    print("="*70 + "\n")
    
    return jsonify({
        "status": "success",
        "campaign_id": campaign.id,
        "campaign_name": strategy.get('campaign_name'),
        "insights": insights,
        "strategy": strategy,
        "daily_content": daily_content
    }), 200