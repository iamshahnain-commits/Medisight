import os
from datetime import datetime

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/medisight.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medisight-dev-secret-key'
    
    # MVP Configuration
    REFERRAL_OVERDUE_DAYS = 5  # Referrals open longer than this are flagged as overdue
    FOLLOWUP_SUGGESTED_DAYS = 7  # Auto-create follow-ups with this offset

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
