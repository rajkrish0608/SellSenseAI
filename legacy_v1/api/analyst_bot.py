from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_services.gemini_ai import create_gemini_ai

analyst_bp = Blueprint('analyst', __name__)


@analyst_bp.route('/api/analyst/analyze', methods=['POST'])
def analyze_sales():
    """
    🔍 ANALYST BOT
    
    Receives:
    - business_profile: {business_name, niche, target_audience, brand_voice}
    - sales_data: [{week, revenue, items_sold, products}]
    
    Returns:
    - best_selling_product
    - revenue_trend
    - customer_insights
    - opportunities
    - recommended_focus
    """
    
    data = request.get_json()
    
    business_profile = data.get('business_profile', {})
    sales_data = data.get('sales_data', [])
    
    print("\n" + "="*70)
    print("🔍 ANALYST BOT - STARTING ANALYSIS")
    print("="*70)
    print(f"Business: {business_profile.get('business_name', 'Unknown')}")
    print(f"Sales Records: {len(sales_data)}")
    
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
    
    # Format sales data for AI
    if sales_data and len(sales_data) > 0:
        sales_summary = "\n".join([
            f"• Week of {sale.get('week', 'N/A')}: ₹{sale.get('revenue', 0):,.0f} revenue, {sale.get('items_sold', 0)} items sold"
            for sale in sales_data
        ])
    else:
        sales_summary = "No sales data available yet. This is a new business."
    
    # Create analyst prompt
    prompt = f"""You are a professional business analyst for small businesses in India.

BUSINESS INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Business Name: {business_profile.get('business_name', 'Unknown Business')}
- Niche/Industry: {business_profile.get('niche', 'General retail')}
- Target Audience: {business_profile.get('target_audience', 'General customers')}
- Brand Voice: {business_profile.get('brand_voice', 'Friendly')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SALES DATA (Last 4 Weeks):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{sales_summary}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK:
Analyze this sales data and provide actionable business insights that will help create effective marketing campaigns.

Return ONLY valid JSON in this exact structure:
{{
  "best_selling_product": {{
    "name": "Product name or category",
    "total_revenue": 0,
    "total_units": 0,
    "trend": "increasing/stable/decreasing"
  }},
  "revenue_trend": {{
    "trend": "up/down/stable",
    "change_percent": 0,
    "direction": "up/down/stable"
  }},
  "customer_insights": [
    "Key insight about customer behavior or preferences",
    "Another important pattern noticed in sales data",
    "Third insight about purchasing habits"
  ],
  "opportunities": [
    "Specific opportunity to increase sales",
    "Another growth opportunity based on data"
  ],
  "recommended_focus": {{
    "product": "Which product or category to promote in campaign",
    "reason": "Why this product is the best focus right now",
    "strategy": "How to maximize this opportunity in marketing"
  }}
}}"""
    
    print("📊 Analyzing sales patterns with Google Gemini...")
    
    # Generate insights using Gemini
    insights = gemini.generate_json(prompt, max_tokens=2000)
    
    if not insights:
        print("⚠️  AI generation failed, using fallback insights")
        insights = get_fallback_insights()
    else:
        print("✅ Analysis generated successfully")
    
    # Log results
    print(f"\n📈 ANALYSIS RESULTS:")
    print(f"   Focus Product: {insights.get('recommended_focus', {}).get('product', 'N/A')}")
    print(f"   Revenue Trend: {insights.get('revenue_trend', {}).get('trend', 'N/A')}")
    print(f"   Key Insights: {len(insights.get('customer_insights', []))}")
    print(f"   Opportunities: {len(insights.get('opportunities', []))}")
    print("="*70 + "\n")
    
    return jsonify(insights), 200


def get_fallback_insights():
    """Fallback insights if AI fails"""
    return {
        "best_selling_product": {
            "name": "Your popular products",
            "total_revenue": 0,
            "total_units": 0,
            "trend": "stable"
        },
        "revenue_trend": {
            "trend": "stable",
            "change_percent": 0,
            "direction": "stable"
        },
        "customer_insights": [
            "Focus on consistent posting schedule to build audience",
            "Engage with followers regularly to boost loyalty and trust",
            "Use high-quality product images to showcase value"
        ],
        "opportunities": [
            "Launch Instagram Stories for higher engagement rates",
            "Post at peak times: 9 AM, 2 PM, and 7 PM for maximum reach"
        ],
        "recommended_focus": {
            "product": "Best-selling products",
            "reason": "They already have proven market demand and customer interest",
            "strategy": "Create social proof and urgency around these popular items"
        }
    }


@analyst_bp.route('/api/analyst/health', methods=['GET'])
def analyst_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "analyst",
        "message": "Analyst Bot is ready"
    }), 200