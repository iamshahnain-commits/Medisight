from app import db
from datetime import datetime, timedelta
from flask import current_app

class Patient(db.Model):
    """Patient model for hospital management"""
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))  # M/F/Other
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    triages = db.relationship('Triage', backref='patient', lazy=True, cascade='all, delete-orphan')
    referrals = db.relationship('Referral', backref='patient', lazy=True, cascade='all, delete-orphan')
    followups = db.relationship('FollowUp', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.patient_id}: {self.name}>'


class Facility(db.Model):
    """Facility (hospital, PHC, sub-center) model"""
    __tablename__ = 'facility'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    facility_type = db.Column(db.String(50))  # PHC, Sub-center, Hospital, etc.
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    referrals_from = db.relationship('Referral', foreign_keys='Referral.from_facility_id', backref='from_facility', lazy=True)
    referrals_to = db.relationship('Referral', foreign_keys='Referral.to_facility_id', backref='to_facility', lazy=True)
    
    def __repr__(self):
        return f'<Facility {self.code}: {self.name}>'


class Triage(db.Model):
    """Triage assessment record"""
    __tablename__ = 'triage'
    
    OUTCOMES = {
        'routine': 'Routine',
        'teleconsult': 'Needs Teleconsultation',
        'in_person': 'Needs In-Person Visit',
        'emergency': 'Emergency Escalation'
    }
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False, index=True)
    symptoms = db.Column(db.Text)  # Free-text description
    symptom_checkboxes = db.Column(db.String(500))  # CSV: fever,cough,chest_pain,etc.
    duration_days = db.Column(db.Integer)  # How many days of symptoms
    risk_factors = db.Column(db.String(500))  # CSV: pregnancy,chronic_illness,elderly,etc.
    triage_result = db.Column(db.String(50), nullable=False)  # Outcome key
    triage_result_display = db.Column(db.String(100), nullable=False)  # Display name
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Triage Patient={self.patient_id} Result={self.triage_result}>'


class Referral(db.Model):
    """Referral tracking record"""
    __tablename__ = 'referral'
    
    STATUS_CHOICES = ['open', 'arrived', 'completed']
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False, index=True)
    from_facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False, index=True)
    to_facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False, index=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Referral {self.id}: {self.from_facility.name} -> {self.to_facility.name}>'
    
    @property
    def is_overdue(self):
        """Check if referral is overdue (open for more than configured days)"""
        if self.status != 'open':
            return False
        days_old = (datetime.utcnow() - self.created_at).days
        return days_old > current_app.config['REFERRAL_OVERDUE_DAYS']
    
    @property
    def days_open(self):
        """Get number of days referral has been open"""
        return (datetime.utcnow() - self.created_at).days


class FollowUp(db.Model):
    """High-risk follow-up queue record"""
    __tablename__ = 'followup'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False, index=True)
    reason = db.Column(db.String(100), nullable=False)  # e.g., "High-risk triage", "Recent referral"
    scheduled_date = db.Column(db.DateTime, nullable=False, index=True)  # When check-in is due
    status = db.Column(db.String(20), default='pending', index=True)  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<FollowUp Patient={self.patient_id} Status={self.status}>'
    
    @property
    def is_due_today(self):
        """Check if follow-up is due today or overdue"""
        if self.status != 'pending':
            return False
        today = datetime.utcnow().date()
        scheduled = self.scheduled_date.date()
        return scheduled <= today
    
    @property
    def days_overdue(self):
        """Get number of days overdue (negative = future)"""
        today = datetime.utcnow().date()
        scheduled = self.scheduled_date.date()
        delta = (today - scheduled).days
        return delta if delta >= 0 else 0
