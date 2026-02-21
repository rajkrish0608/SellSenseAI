"""
Bot Integration API
Handles WhatsApp bot integration
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json

from database.models import db, SalesUpdate, User

bot_bp = Blueprint('bot', __name__)


@bot_bp.route('/api/sales/update-from-bot', methods=['POST'])
def update_sales_from_bot():
    """Receive sales update from WhatsApp bot"""
    
    data = request.get_json()
    
    message = data.get('message', '')
    seller_phone = data.get('seller_phone', '')
    
    # Find user by phone
    user = User.query.filter_by(phone=seller_phone).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Simple parsing (you can enhance with AI)
    try:
        # Example: "5 rings sold for ₹10000"
        parts = message.split()
        quantity = int(parts[0])
        product_name = parts[1]
        revenue = float(parts[-1].replace('₹', '').replace(',', ''))
        
        products = [{
            "product_name": product_name,
            "quantity": quantity,
            "revenue": revenue
        }]
        
        sale = SalesUpdate(
            user_id=user.id,
            week_start_date=datetime.utcnow().date(),
            products_sold=json.dumps(products),
            source='whatsapp_bot'
        )
        
        sale.calculate_totals()
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Recorded {quantity} {product_name} for ₹{revenue}"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not parse message"}), 400