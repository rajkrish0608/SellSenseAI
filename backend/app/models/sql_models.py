from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Float, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    sales_updates = relationship("SalesUpdate", back_populates="user", cascade="all, delete-orphan")

class BusinessProfile(Base):
    __tablename__ = 'business_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    business_name = Column(String, nullable=False)
    niche = Column(String)
    target_audience = Column(String)
    brand_voice = Column(String, default='Friendly')
    product_catalog = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="business_profile")

class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)
    status = Column(String, default='draft')
    strategy_data = Column(Text)  # JSON
    insights_data = Column(Text)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="campaigns")
    content_pieces = relationship("CampaignContent", back_populates="campaign", cascade="all, delete-orphan")

class CampaignContent(Base):
    __tablename__ = 'campaign_content'
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    day_number = Column(Integer, nullable=False)
    content_type = Column(String)
    caption = Column(Text)
    image_prompt = Column(Text)
    video_url = Column(String)  # New: URL to the generated AI video
    audio_url = Column(String)  # New: URL to the generated AI voiceover
    is_posted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="content_pieces")

class SalesUpdate(Base):
    __tablename__ = 'sales_updates'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week_start_date = Column(Date, nullable=False)
    products_sold = Column(Text) # JSON
    total_revenue = Column(Float, default=0)
    total_items_sold = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="sales_updates")

class Trend(Base):
    __tablename__ = 'trends'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String)  # 'audio', 'hashtag', 'topic'
    source = Column(String) # 'tiktok', 'instagram'
    relevance_score = Column(Float, default=0)
    discovery_date = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(Text) # JSON string for audio link, viz, etc.

class AdCampaign(Base):
    __tablename__ = 'ad_campaigns'
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    platform = Column(String) # 'meta', 'google', 'tiktok'
    ad_id = Column(String) # External ID
    budget = Column(Float)
    status = Column(String) # 'active', 'paused', 'completed'
    auto_pilot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AdPerformance(Base):
    __tablename__ = 'ad_performance'
    
    id = Column(Integer, primary_key=True, index=True)
    ad_campaign_id = Column(Integer, ForeignKey('ad_campaigns.id'), nullable=False)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    spend = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.utcnow)
