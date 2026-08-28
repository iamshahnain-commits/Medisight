from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.patients.routes import patients_bp
    from app.triage.routes import triage_bp
    from app.referrals.routes import referrals_bp
    from app.followups.routes import followups_bp
    from app.dashboard.routes import dashboard_bp
    from app.main.routes import main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(triage_bp)
    app.register_blueprint(referrals_bp)
    app.register_blueprint(followups_bp)
    app.register_blueprint(dashboard_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
