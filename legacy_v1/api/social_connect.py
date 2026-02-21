"""
Social Media Account Connection
Handles Instagram, Facebook, WhatsApp connections
"""

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime

from database.models import db, SocialAccount

social_bp = Blueprint('social', __name__)


@social_bp.route('/connect-accounts', methods=['GET'])
@login_required
def connect_accounts_page():
    """Social accounts connection page"""
    return render_template('connect_accounts.html')


@social_bp.route('/api/social/connect/instagram', methods=['POST'])
@login_required
def connect_instagram():
    """Connect Instagram Business account"""
    
    data = request.get_json()
    
    access_token = data.get('access_token')
    business_id = data.get('business_id')
    
    if not access_token or not business_id:
        return jsonify({"error": "Access token and business ID required"}), 400
    
    try:
        # Check if already connected
        existing = SocialAccount.query.filter_by(
            user_id=current_user.id,
            platform='instagram'
        ).first()
        
        if existing:
            existing.access_token = access_token
            existing.account_id = business_id
            existing.is_active = True
            existing.connected_at = datetime.utcnow()
        else:
            account = SocialAccount(
                user_id=current_user.id,
                platform='instagram',
                account_id=business_id,
                access_token=access_token,
                is_active=True
            )
            db.session.add(account)
        
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Instagram connected!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@social_bp.route('/api/social/connect/facebook', methods=['POST'])
@login_required
def connect_facebook():
    """Connect Facebook Page"""
    
    data = request.get_json()
    
    access_token = data.get('access_token')
    page_id = data.get('page_id')
    
    if not access_token or not page_id:
        return jsonify({"error": "Access token and page ID required"}), 400
    
    try:
        existing = SocialAccount.query.filter_by(
            user_id=current_user.id,
            platform='facebook'
        ).first()
        
        if existing:
            existing.access_token = access_token
            existing.account_id = page_id
            existing.is_active = True
        else:
            account = SocialAccount(
                user_id=current_user.id,
                platform='facebook',
                account_id=page_id,
                access_token=access_token,
                is_active=True
            )
            db.session.add(account)
        
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Facebook connected!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@social_bp.route('/api/social/disconnect/<platform>', methods=['DELETE'])
@login_required
def disconnect_account(platform):
    """Disconnect social account"""
    
    account = SocialAccount.query.filter_by(
        user_id=current_user.id,
        platform=platform
    ).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    try:
        db.session.delete(account)
        db.session.commit()
        
        return jsonify({"status": "success", "message": f"{platform} disconnected"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500