from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from database.models import db, PostHistory, Campaign

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics', methods=['GET'])
@login_required
def analytics_page():
    """Analytics dashboard page"""
    return render_template('analytics_dashboard.html')


@analytics_bp.route('/api/analytics/dashboard', methods=['GET'])
@login_required
def get_analytics_dashboard():
    """Get analytics dashboard data"""
    
    platform = request.args.get('platform', 'all')
    
    # Get posts from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    query = PostHistory.query.filter_by(user_id=current_user.id)
    
    if platform != 'all':
        query = query.filter_by(platform=platform)
    
    posts = query.filter(PostHistory.posted_at >= thirty_days_ago).all()
    
    # Calculate metrics
    total_reach = sum(p.reach for p in posts)
    total_posts = len(posts)
    avg_engagement = sum(p.engagement_rate for p in posts) / total_posts if total_posts > 0 else 0
    
    # Get top posts
    top_posts = sorted(posts, key=lambda x: x.engagement_rate, reverse=True)[:5]
    
    return jsonify({
        "total_reach": total_reach,
        "total_posts": total_posts,
        "avg_engagement_rate": round(avg_engagement, 2),
        "top_posts": [{
            "caption": p.caption[:100],
            "platform": p.platform,
            "likes": p.likes,
            "comments": p.comments,
            "engagement_rate": p.engagement_rate,
            "posted_at": p.posted_at.isoformat() if p.posted_at else None
        } for p in top_posts]
    })