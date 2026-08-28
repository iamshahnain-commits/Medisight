from datetime import datetime, timedelta
from app.models import Referral, FollowUp, Triage
from app import db

def get_overdue_referrals():
    """Get all open referrals that are overdue"""
    return Referral.query.filter_by(status='open').all() and [
        r for r in Referral.query.filter_by(status='open').all() if r.is_overdue
    ]

def get_followups_due_today():
    """Get all follow-ups due today or overdue"""
    return [f for f in FollowUp.query.filter_by(status='pending').all() if f.is_due_today]

def create_followup_for_patient(patient_id, reason, offset_days=7):
    """Create a follow-up record for a patient, avoiding duplicates
    
    Args:
        patient_id: Patient ID
        reason: Reason for follow-up
        offset_days: Days from now to schedule the follow-up
    
    Returns:
        FollowUp object or None if duplicate exists
    """
    scheduled_date = datetime.utcnow() + timedelta(days=offset_days)
    
    # Check for existing pending follow-up with same reason created recently
    existing = FollowUp.query.filter_by(
        patient_id=patient_id,
        reason=reason,
        status='pending'
    ).first()
    
    if existing:
        # Follow-up for this reason already exists
        return None
    
    followup = FollowUp(
        patient_id=patient_id,
        reason=reason,
        scheduled_date=scheduled_date
    )
    db.session.add(followup)
    db.session.commit()
    return followup

def mark_followup_completed(followup_id):
    """Mark a follow-up as completed"""
    followup = FollowUp.query.get(followup_id)
    if followup:
        followup.status = 'completed'
        followup.completed_at = datetime.utcnow()
        db.session.commit()
    return followup
