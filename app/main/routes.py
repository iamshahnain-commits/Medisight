from flask import Blueprint, render_template
from app.models import Patient, Triage, Referral, FollowUp
from app.utils import get_overdue_referrals, get_followups_due_today

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page with dashboard summary"""
    total_patients = Patient.query.count()
    recent_triages = Triage.query.order_by(Triage.created_at.desc()).limit(5).all()
    overdue_referrals = get_overdue_referrals()
    followups_due = get_followups_due_today()
    
    return render_template('main/index.html',
                         total_patients=total_patients,
                         recent_triages=recent_triages,
                         overdue_referrals=overdue_referrals,
                         followups_due=followups_due)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')
