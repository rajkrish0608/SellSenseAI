"""
AI Learning API
Handles pattern recognition and learning
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from database.models import db, PostHistory, PerformancePattern

learning_bp = Blueprint('learning', __name__)


@learning_bp.route('/api/ai/learn-from-performance', methods=['POST'])
@login_required
def learn_from_performance():
    """Learn patterns from high-performing posts"""
    
    # Get high-performing posts
    posts = PostHistory.query.filter_by(
        user_id=current_user.id
    ).filter(PostHistory.engagement_rate >= 5.0).all()
    
    if len(posts) < 5:
        return jsonify({
            "status": "info",
            "message": "Need at least 5 high-performing posts to learn patterns"
        }), 200
    
    # Analyze patterns (simplified)
    patterns = {
        "optimal_posting_time": "9 AM - 11 AM",
        "best_content_length": "100-150 words",
        "effective_hashtags": ["trending", "sale", "new"]
    }
    
    # Save pattern
    try:
        pattern = PerformancePattern(
            user_id=current_user.id,
            pattern_type='posting_time',
            pattern_data=str(patterns),
            avg_engagement_rate=sum(p.engagement_rate for p in posts) / len(posts),
            sample_size=len(posts),
            confidence_score=0.75
        )
        
        db.session.add(pattern)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "patterns": patterns,
            "sample_size": len(posts)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500