"""
Database Models
All SQLAlchemy models for the application
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    business_profile = db.relationship('BusinessProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    sales_updates = db.relationship('SalesUpdate', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    campaigns = db.relationship('Campaign', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    social_accounts = db.relationship('SocialAccount', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    posts = db.relationship('PostHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class BusinessProfile(db.Model):
    """Business profile model"""
    __tablename__ = 'business_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    business_name = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(100))
    target_audience = db.Column(db.String(200))
    brand_voice = db.Column(db.String(50), default='Friendly')
    product_catalog = db.Column(db.Text)  # JSON string
    primary_goal = db.Column(db.String(50))
    monthly_target_revenue = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BusinessProfile {self.business_name}>'


class SalesUpdate(db.Model):
    """Sales update model"""
    __tablename__ = 'sales_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False, index=True)
    products_sold = db.Column(db.Text)  # JSON array
    total_revenue = db.Column(db.Float, default=0)
    total_items_sold = db.Column(db.Integer, default=0)
    seller_notes = db.Column(db.Text)
    whatsapp_conversations = db.Column(db.Integer, default=0)
    whatsapp_sales_closed = db.Column(db.Integer, default=0)
    source = db.Column(db.String(20), default='manual')  # manual, whatsapp_bot
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_totals(self):
        """Calculate total revenue and items from products_sold"""
        if self.products_sold:
            try:
                products = json.loads(self.products_sold) if isinstance(self.products_sold, str) else self.products_sold
                self.total_revenue = sum(p.get('revenue', 0) for p in products)
                self.total_items_sold = sum(p.get('quantity', 0) for p in products)
            except:
                pass
    
    def __repr__(self):
        return f'<SalesUpdate {self.week_start_date} - ₹{self.total_revenue}>'


class Campaign(db.Model):
    """Campaign model"""
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    campaign_name = db.Column(db.String(200), nullable=False)
    campaign_type = db.Column(db.String(50))  # flash_sale, product_launch, etc.
    duration_days = db.Column(db.Integer, default=7)
    strategy = db.Column(db.Text)  # JSON string
    insights = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(20), default='draft')  # draft, active, completed
    total_reach = db.Column(db.Integer, default=0)
    total_engagement = db.Column(db.Integer, default=0)
    total_sales_attributed = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    content_pieces = db.relationship('CampaignContent', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    assets = db.relationship('CampaignAsset', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    posts = db.relationship('PostHistory', backref='campaign', lazy='dynamic')
    
    def __repr__(self):
        return f'<Campaign {self.campaign_name}>'


class CampaignContent(db.Model):
    """Campaign content model"""
    __tablename__ = 'campaign_content'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(50))  # instagram_post, whatsapp_message, story
    caption = db.Column(db.Text)
    whatsapp_message = db.Column(db.Text)
    story_script = db.Column(db.Text)  # JSON string
    variant = db.Column(db.String(10))  # A, B for A/B testing
    theme = db.Column(db.String(100))
    scheduled_time = db.Column(db.DateTime)
    is_posted = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    reach = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CampaignContent Day {self.day_number}>'


class CampaignAsset(db.Model):
    """Campaign asset model (images, videos)"""
    __tablename__ = 'campaign_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    asset_type = db.Column(db.String(20))  # image, video
    file_path = db.Column(db.String(500))
    file_url = db.Column(db.String(500))
    day_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CampaignAsset {self.asset_type}>'


class SocialAccount(db.Model):
    """Social media account model"""
    __tablename__ = 'social_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(20), nullable=False)  # instagram, facebook, whatsapp
    account_id = db.Column(db.String(100))
    account_name = db.Column(db.String(200))
    access_token = db.Column(db.Text)
    token_expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sync = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SocialAccount {self.platform} - {self.account_name}>'


class PostHistory(db.Model):
    """Post history model"""
    __tablename__ = 'post_history'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('campaign_content.id'))
    platform = db.Column(db.String(20), nullable=False)  # instagram, facebook, whatsapp
    post_type = db.Column(db.String(20))  # feed, story, reel
    caption = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    platform_post_id = db.Column(db.String(100))
    permalink = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    reach = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)
    saves = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='published')
    scheduled_for = db.Column(db.DateTime)
    posted_at = db.Column(db.DateTime)
    variant = db.Column(db.String(10))  # A, B
    is_winner = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PostHistory {self.platform} - {self.posted_at}>'


class PerformancePattern(db.Model):
    """Performance pattern model (AI learning)"""
    __tablename__ = 'performance_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pattern_type = db.Column(db.String(50))  # posting_time, caption_style, content_theme
    pattern_data = db.Column(db.Text)  # JSON string
    avg_engagement_rate = db.Column(db.Float)
    sample_size = db.Column(db.Integer)
    confidence_score = db.Column(db.Float)
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PerformancePattern {self.pattern_type}>'


class AIPromptEvolution(db.Model):
    """AI prompt evolution model"""
    __tablename__ = 'ai_prompt_evolution'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt_type = db.Column(db.String(50))  # caption, strategy, analysis
    original_prompt = db.Column(db.Text)
    evolved_prompt = db.Column(db.Text)
    performance_score = db.Column(db.Float)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIPromptEvolution {self.prompt_type}>'


class CustomerInteraction(db.Model):
    """Customer interaction model"""
    __tablename__ = 'customer_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(20))  # whatsapp, instagram, facebook
    customer_phone = db.Column(db.String(20))
    customer_name = db.Column(db.String(100))
    message_text = db.Column(db.Text)
    intent = db.Column(db.String(50))  # inquiry, purchase, complaint
    sentiment = db.Column(db.String(20))  # positive, neutral, negative
    response_sent = db.Column(db.Text)
    converted_to_sale = db.Column(db.Boolean, default=False)
    sale_amount = db.Column(db.Float)
    interaction_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CustomerInteraction {self.platform} - {self.interaction_at}>'