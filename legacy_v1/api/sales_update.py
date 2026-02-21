from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
import json

from database.models import db, SalesUpdate

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/sales/update', methods=['GET'])
@login_required
def sales_update_page():
    """Sales update page"""
    return render_template('sales_update.html')


@sales_bp.route('/api/sales/update', methods=['POST'])
@login_required
def create_sales_update():
    """Create a new sales update"""
    
    data = request.get_json()
    
    week_start = data.get('week_start_date')
    products = data.get('products', [])
    whatsapp_convos = data.get('whatsapp_conversations', 0)
    notes = data.get('notes', '')
    
    if not week_start:
        return jsonify({"error": "Week start date required"}), 400
    
    try:
        # Create sales update
        sale = SalesUpdate(
            user_id=current_user.id,
            week_start_date=datetime.fromisoformat(week_start).date(),
            products_sold=json.dumps(products),
            whatsapp_conversations=whatsapp_convos,
            seller_notes=notes,
            source='manual'
        )
        
        # Calculate totals
        sale.calculate_totals()
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Sales update added successfully",
            "total_revenue": sale.total_revenue,
            "total_items": sale.total_items_sold
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@sales_bp.route('/api/sales/latest', methods=['GET'])
@login_required
def get_latest_sales():
    """Get latest sales update"""
    
    latest = SalesUpdate.query.filter_by(
        user_id=current_user.id
    ).order_by(SalesUpdate.week_start_date.desc()).first()
    
    if not latest:
        return jsonify({"message": "No sales data yet"}), 404
    
    return jsonify({
        "week_start_date": latest.week_start_date.isoformat(),
        "total_revenue": latest.total_revenue,
        "total_items_sold": latest.total_items_sold,
        "products_sold": json.loads(latest.products_sold) if latest.products_sold else []
    })


@sales_bp.route('/api/sales/history', methods=['GET'])
@login_required
def get_sales_history():
    """Get sales history (last 4 weeks)"""
    
    history = SalesUpdate.query.filter_by(
        user_id=current_user.id
    ).order_by(SalesUpdate.week_start_date.desc()).limit(4).all()
    
    return jsonify([{
        "week_start_date": sale.week_start_date.isoformat(),
        "total_revenue": sale.total_revenue,
        "total_items_sold": sale.total_items_sold
    } for sale in history])