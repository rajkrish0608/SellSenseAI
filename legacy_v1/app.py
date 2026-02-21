"""
Agentic Sales AI - Complete Application
Multi-Agent AI System for Social Media Marketing

Features:
- 3 AI Agents (Analyst, Strategy, Content)
- Google Gemini Integration (FREE)
- n8n Workflow Automation
- Modern Dark UI
- Campaign Generation
- Analytics Dashboard
- Social Media Integration
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import configuration
from config import config

# Import database models
from database.models import (
    db, User, BusinessProfile, SalesUpdate, Campaign, 
    CampaignContent, PostHistory, SocialAccount
)

# Import ALL API blueprints
from api.sales_update import sales_bp
from api.bot_integration import bot_bp
from api.social_connect import social_bp
from api.n8n_integration import n8n_bp
from api.analytics import analytics_bp
from api.ai_learning import learning_bp
from api.auth_reset import auth_reset_bp

# Import AI Agent blueprints
from api.analyst_bot import analyst_bp
from api.strategy_bot import strategy_bp
from api.content_bot import content_bp

# ============================================
# FLASK APP INITIALIZATION
# ============================================

app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

print("\n" + "="*70)
print("🚀 AGENTIC SALES AI - INITIALIZING")
print("="*70)
print(f"Environment: {env}")
print(f"Debug Mode: {app.config['DEBUG']}")
print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ============================================
# REGISTER ALL BLUEPRINTS
# ============================================

# Main API blueprints
app.register_blueprint(sales_bp)
app.register_blueprint(bot_bp)
app.register_blueprint(social_bp)
app.register_blueprint(n8n_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(auth_reset_bp)

# AI Agent blueprints (for n8n integration)
app.register_blueprint(analyst_bp)
app.register_blueprint(strategy_bp)
app.register_blueprint(content_bp)

print("✅ All blueprints registered successfully")
print("   • Sales Update")
print("   • Bot Integration")
print("   • Social Connect")
print("   • n8n Integration")
print("   • Analytics")
print("   • AI Learning")
print("   • Auth Reset")
print("   • Analyst Bot (AI Agent)")
print("   • Strategy Bot (AI Agent)")
print("   • Content Bot (AI Agent)")


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/')
def index():
    """Home page - redirect based on auth status"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            business_name = user.business_profile.business_name if user.business_profile else user.email
            flash(f'Welcome back, {business_name}! 🎉', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        business_name = request.form.get('business_name', '').strip()
        niche = request.form.get('niche', '').strip()
        target_audience = request.form.get('target_audience', '').strip()
        brand_voice = request.form.get('brand_voice', 'Friendly')
        
        # Validation
        if not email or not password or not business_name:
            flash('Please fill in all required fields.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('signup.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login instead.', 'error')
            return render_template('signup.html')
        
        try:
            # Create user
            user = User(email=email, phone=phone)
            user.set_password(password)
            
            db.session.add(user)
            db.session.flush()
            
            # Create business profile
            profile = BusinessProfile(
                user_id=user.id,
                business_name=business_name,
                niche=niche,
                target_audience=target_audience,
                brand_voice=brand_voice
            )
            
            db.session.add(profile)
            db.session.commit()
            
            # Auto-login
            login_user(user)
            
            flash(f'Welcome to Agentic Sales AI, {business_name}! 🎉', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))


# ============================================
# MAIN APPLICATION ROUTES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', now=datetime.now())


@app.route('/api/dashboard/summary')
@login_required
def dashboard_summary():
    """
    Get dashboard summary data
    Returns: JSON with stats, charts data, recent activity
    """
    
    # Get this week's sales
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    this_week_sales = SalesUpdate.query.filter(
        SalesUpdate.user_id == current_user.id,
        SalesUpdate.week_start_date >= week_start
    ).all()
    
    # Calculate metrics
    week_revenue = sum(sale.total_revenue for sale in this_week_sales)
    items_sold = sum(sale.total_items_sold for sale in this_week_sales)
    
    # Get last week for comparison
    last_week_start = week_start - timedelta(days=7)
    last_week_sales = SalesUpdate.query.filter(
        SalesUpdate.user_id == current_user.id,
        SalesUpdate.week_start_date >= last_week_start,
        SalesUpdate.week_start_date < week_start
    ).all()
    
    last_week_revenue = sum(sale.total_revenue for sale in last_week_sales)
    last_week_items = sum(sale.total_items_sold for sale in last_week_sales)
    
    # Calculate changes
    revenue_change = ((week_revenue - last_week_revenue) / last_week_revenue * 100) if last_week_revenue > 0 else 0
    items_change = items_sold - last_week_items
    
    # Get active campaigns
    active_campaigns = Campaign.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).count()
    
    # Get engagement rate from recent posts
    recent_posts = PostHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(PostHistory.posted_at.desc()).limit(10).all()
    
    avg_engagement = sum(p.engagement_rate for p in recent_posts) / len(recent_posts) if recent_posts else 0
    
    # Revenue timeline (last 7 days)
    timeline_labels = []
    timeline_values = []
    
    for i in range(7):
        day = today - timedelta(days=6-i)
        day_sales = [s for s in this_week_sales if s.week_start_date == day]
        day_revenue = sum(s.total_revenue for s in day_sales)
        
        timeline_labels.append(day.strftime('%a'))
        timeline_values.append(day_revenue)
    
    # Top products
    all_products = {}
    for sale in this_week_sales:
        if sale.products_sold:
            try:
                import json
                products = json.loads(sale.products_sold) if isinstance(sale.products_sold, str) else sale.products_sold
                for product in products:
                    name = product.get('product_name', 'Unknown')
                    qty = product.get('quantity', 0)
                    all_products[name] = all_products.get(name, 0) + qty
            except:
                pass
    
    top_products = sorted(all_products.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Recent activity
    recent_activity = []
    
    if week_revenue > 0:
        recent_activity.append({
            'icon': '💰',
            'title': 'Sales Update',
            'description': f'Added ₹{week_revenue:,.0f} in sales this week',
            'time': '2 hours ago'
        })
    
    recent_campaigns = Campaign.query.filter_by(user_id=current_user.id).order_by(Campaign.created_at.desc()).limit(1).all()
    if recent_campaigns:
        recent_activity.append({
            'icon': '🎯',
            'title': 'Campaign Created',
            'description': f'New campaign: {recent_campaigns[0].campaign_name}',
            'time': '1 day ago'
        })
    
    if avg_engagement > 0:
        recent_activity.append({
            'icon': '📈',
            'title': 'Engagement Up',
            'description': f'Engagement rate at {avg_engagement:.1f}%',
            'time': '2 days ago'
        })
    
    return jsonify({
        'week_revenue': week_revenue,
        'items_sold': items_sold,
        'active_campaigns': active_campaigns,
        'engagement_rate': round(avg_engagement, 1),
        'revenue_change': round(revenue_change, 1),
        'items_change': items_change,
        'engagement_change': 5.2,
        'revenue_timeline': {
            'labels': timeline_labels,
            'values': timeline_values
        },
        'top_products': {
            'labels': [p[0] for p in top_products],
            'values': [p[1] for p in top_products]
        },
        'recent_activity': recent_activity
    })


@app.route('/generate-campaign')
@login_required
def generate_campaign_page():
    """Campaign generation page"""
    return render_template('generate_campaign.html')


# ============================================
# DEMO / HACKATHON ROUTES
# ============================================

@app.route('/demo')
def demo_hub():
    """
    Demo hub - central access point for hackathon presentation
    Shows all demo features with quick links
    """
    return render_template('demo_hub.html')


@app.route('/demo/live')
def live_demo():
    """
    Live demo dashboard for hackathon presentation
    Shows 3 AI agents working in real-time
    """
    return render_template('live_dashboard.html')


@app.route('/demo/architecture')
def architecture():
    """
    System architecture visualization
    Shows technical architecture with diagrams
    """
    return render_template('architecture.html')


@app.route('/api/demo/metrics')
def demo_metrics():
    """
    Get demo metrics for hackathon
    Returns: Overall system statistics
    """
    
    total_campaigns = Campaign.query.count()
    total_users = User.query.count()
    total_posts = PostHistory.query.count()
    
    return jsonify({
        "total_campaigns": total_campaigns,
        "total_posts": total_posts,
        "total_users": total_users,
        "total_content_pieces": total_campaigns * 7,
        "avg_processing_time": 23,
        "cost_per_campaign": 0,
        "cost_savings": 50000 * total_campaigns,
        "time_saved_hours": 10 * total_campaigns
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    if request.path.startswith('/api/'):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found"
        }), 404
    return jsonify({"error": "Page not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(403)
def forbidden(error):
    """403 error handler"""
    if request.path.startswith('/api/'):
        return jsonify({
            "status": "error",
            "message": "Access forbidden"
        }), 403
    return jsonify({"error": "Forbidden"}), 403


# ============================================
# HEALTH CHECK & STATUS
# ============================================

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        
        return jsonify({
            "status": "healthy",
            "version": "1.0.0",
            "environment": env,
            "database": "connected",
            "agents": ["analyst", "strategy", "content"],
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


@app.route('/api/status')
def api_status():
    """API status endpoint"""
    
    # Check AI availability
    ai_status = "unknown"
    try:
        from ai_services.gemini_ai import create_gemini_ai
        gemini = create_gemini_ai()
        ai_status = "available"
    except:
        ai_status = "unavailable"
    
    return jsonify({
        "status": "operational",
        "ai_engine": "Google Gemini",
        "ai_status": ai_status,
        "endpoints": {
            "analyst": "/api/analyst/analyze",
            "strategy": "/api/strategy/create",
            "content": "/api/content/generate",
            "campaign": "/api/campaign/generate"
        },
        "features": [
            "Multi-agent AI",
            "Campaign generation",
            "Sales analytics",
            "Social media integration",
            "n8n automation"
        ]
    })


# ============================================
# DATABASE INITIALIZATION
# ============================================

with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables initialized")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")


# ============================================
# APPLICATION STARTUP
# ============================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 AGENTIC SALES AI - SERVER STARTING")
    print("="*70)
    print(f"\n📍 Application URL:")
    print(f"   http://localhost:5000")
    print(f"\n🎯 Demo URLs:")
    print(f"   Demo Hub:      http://localhost:5000/demo")
    print(f"   Live Demo:     http://localhost:5000/demo/live")
    print(f"   Architecture:  http://localhost:5000/demo/architecture")
    print(f"\n✨ Features Available:")
    print(f"   • User Authentication (Signup/Login)")
    print(f"   • 3 AI Agents (Analyst, Strategy, Content)")
    print(f"   • Campaign Generation (Google Gemini - FREE)")
    print(f"   • Sales Tracking & Analytics")
    print(f"   • Social Media Integration")
    print(f"   • n8n Workflow Automation")
    print(f"   • Modern Dark UI Dashboard")
    print(f"\n🤖 AI Agents Ready:")
    print(f"   • Analyst Bot:  /api/analyst/analyze")
    print(f"   • Strategy Bot: /api/strategy/create")
    print(f"   • Content Bot:  /api/content/generate")
    print(f"\n⚙️  Environment:")
    print(f"   Mode: {env}")
    print(f"   Debug: {app.config['DEBUG']}")
    print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('///')[-1]}")
    
    # Check for API key
    if not os.getenv('GOOGLE_GEMINI_API_KEY'):
        print(f"\n⚠️  WARNING: GOOGLE_GEMINI_API_KEY not set!")
        print(f"   Add your API key to .env file")
        print(f"   Get FREE key: https://makersuite.google.com/app/apikey")
    else:
        print(f"\n✅ Google Gemini API key configured")
    
    print(f"\n" + "="*70)
    print("⌨️  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Run the application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )