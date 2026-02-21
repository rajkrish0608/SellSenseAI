"""
Test n8n Workflow
Complete test script for the 3-agent workflow
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
N8N_WEBHOOK = os.getenv('N8N_CAMPAIGN_WEBHOOK', 'http://localhost:5678/webhook/campaign-3-agents')

# Test payload
test_data = {
    "business_profile": {
        "business_name": "Sparkle & Shine Jewelry",
        "niche": "Handmade Jewelry",
        "target_audience": "Women 25-40, fashion-conscious",
        "brand_voice": "Elegant & Friendly"
    },
    "campaign_goal": "flash_sale",
    "sales_data": [
        {
            "week": "2026-02-10",
            "revenue": 45000,
            "items_sold": 58,
            "products": [
                {"product_name": "Silver Rings", "quantity": 25, "revenue": 20000},
                {"product_name": "Gold Necklaces", "quantity": 15, "revenue": 15000},
                {"product_name": "Diamond Earrings", "quantity": 18, "revenue": 10000}
            ]
        },
        {
            "week": "2026-02-03",
            "revenue": 38000,
            "items_sold": 42,
            "products": [
                {"product_name": "Silver Rings", "quantity": 20, "revenue": 16000},
                {"product_name": "Gold Necklaces", "quantity": 12, "revenue": 12000},
                {"product_name": "Diamond Earrings", "quantity": 10, "revenue": 10000}
            ]
        }
    ]
}


def test_workflow():
    """Test the complete n8n 3-agent workflow"""
    
    print("\n" + "="*80)
    print("🧪 TESTING N8N 3-AGENT WORKFLOW")
    print("="*80)
    print(f"\n📡 Webhook URL: {N8N_WEBHOOK}")
    print(f"🏢 Business: {test_data['business_profile']['business_name']}")
    print(f"🎯 Goal: {test_data['campaign_goal']}")
    print(f"📊 Sales Records: {len(test_data['sales_data'])}")
    
    print("\n" + "-"*80)
    print("📤 Sending request to n8n workflow...")
    print("-"*80)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            N8N_WEBHOOK,
            json=test_data,
            timeout=180  # 3 minutes
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n⏱️  Response received in {elapsed:.1f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.ok:
            result = response.json()
            
            print("\n" + "="*80)
            print("✅ SUCCESS! WORKFLOW COMPLETED")
            print("="*80)
            
            # Display results
            print(f"\n🎯 Campaign Name: {result.get('campaign_name', 'N/A')}")
            print(f"📊 Campaign Type: {result.get('campaign_type', 'N/A')}")
            print(f"🏆 Focus Product: {result.get('focus_product', 'N/A')}")
            print(f"📅 Total Days: {result.get('total_days', 0)}")
            print(f"🤖 Agents Used: {', '.join(result.get('agents_used', []))}")
            print(f"🕐 Generated At: {result.get('generated_at', 'N/A')}")
            
            # Show insights
            if result.get('insights'):
                print("\n" + "-"*80)
                print("🔍 ANALYST INSIGHTS:")
                print("-"*80)
                insights = result['insights']
                print(f"• Revenue Trend: {insights.get('revenue_trend', {}).get('trend', 'N/A')}")
                if insights.get('customer_insights'):
                    print(f"• Key Insights: {len(insights['customer_insights'])} insights generated")
                    for i, insight in enumerate(insights['customer_insights'][:3], 1):
                        print(f"  {i}. {insight}")
            
            # Show strategy
            if result.get('strategy'):
                print("\n" + "-"*80)
                print("🧠 CAMPAIGN STRATEGY:")
                print("-"*80)
                strategy = result['strategy']
                print(f"• Primary Objective: {strategy.get('primary_objective', 'N/A')}")
                print(f"• Key Message: {strategy.get('key_message', 'N/A')}")
                if strategy.get('daily_plan'):
                    print(f"• Daily Themes:")
                    for day in strategy['daily_plan'][:3]:
                        print(f"  Day {day.get('day')}: {day.get('theme')}")
            
            # Show content
            if result.get('daily_content'):
                print("\n" + "-"*80)
                print("🎨 GENERATED CONTENT:")
                print("-"*80)
                for day in result['daily_content'][:3]:
                    print(f"\n📅 Day {day.get('day')}: {day.get('theme', 'N/A')}")
                    caption = day.get('instagram_caption', 'N/A')
                    preview = caption[:80] + "..." if len(caption) > 80 else caption
                    print(f"   Caption: {preview}")
                
                if len(result['daily_content']) > 3:
                    print(f"\n   ... and {len(result['daily_content']) - 3} more days")
            
            print("\n" + "="*80)
            print("🎉 ALL 3 AGENTS EXECUTED SUCCESSFULLY!")
            print("="*80)
            
            # Save result
            with open('workflow_test_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n💾 Full result saved to: workflow_test_result.json")
            
            return True
            
        else:
            print("\n" + "="*80)
            print("❌ WORKFLOW FAILED")
            print("="*80)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.Timeout:
        print("\n" + "="*80)
        print("⏳ REQUEST TIMED OUT")
        print("="*80)
        print("The workflow might still be running.")
        print(f"Check n8n executions: {N8N_WEBHOOK.replace('/webhook/', '/')}")
        return False
        
    except requests.ConnectionError:
        print("\n" + "="*80)
        print("❌ CONNECTION ERROR")
        print("="*80)
        print("Cannot connect to n8n webhook.")
        print(f"Make sure:")
        print("1. n8n is running")
        print("2. Workflow is activated")
        print("3. Webhook URL is correct in .env")
        print(f"   Current: {N8N_WEBHOOK}")
        return False
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ ERROR: {e}")
        print("="*80)
        return False


if __name__ == "__main__":
    success = test_workflow()
    print("\n")
    exit(0 if success else 1)