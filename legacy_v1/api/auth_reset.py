"""
Authentication & Password Reset
"""

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta
import secrets

from database.models import db, User

auth_reset_bp = Blueprint('auth_reset', __name__)

# In-memory token storage (use Redis in production)
reset_tokens = {}


@auth_reset_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        # Generate token
        token = secrets.token_urlsafe(32)
        reset_tokens[token] = {
            'user_id': user.id,
            'expires': datetime.utcnow() + timedelta(hours=1)
        }
        
        # In production, send email with reset link
        reset_link = f"/reset-password/{token}"
        
        return jsonify({
            "status": "success",
            "message": "Reset link sent (check console)",
            "reset_link": reset_link  # Only for demo
        }), 200
    
    # Always return success to prevent email enumeration
    return jsonify({
        "status": "success",
        "message": "If email exists, reset link sent"
    }), 200


@auth_reset_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    
    if request.method == 'GET':
        return render_template('reset_password.html', token=token)
    
    # POST - actually reset password
    data = request.get_json()
    new_password = data.get('password', '')
    
    # Validate token
    if token not in reset_tokens:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    token_data = reset_tokens[token]
    
    if datetime.utcnow() > token_data['expires']:
        del reset_tokens[token]
        return jsonify({"error": "Token expired"}), 400
    
    # Reset password
    user = User.query.get(token_data['user_id'])
    
    if user:
        user.set_password(new_password)
        db.session.commit()
        
        # Delete token
        del reset_tokens[token]
        
        return jsonify({
            "status": "success",
            "message": "Password reset successfully"
        }), 200
    
    return jsonify({"error": "User not found"}), 404