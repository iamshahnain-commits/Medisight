"""Tests for referral overdue calculation"""
import pytest
from datetime import datetime, timedelta
from app import db
from app.models import Patient, Facility, Referral

class TestReferralOverdueCalculation:
    """Test overdue referral detection"""
    
    def test_open_referral_over_5_days_is_overdue(self, app, test_patient, test_facilities):
        """Open referral >5 days old should be marked overdue"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='open',
                created_at=datetime.utcnow() - timedelta(days=6)
            )
            db.session.add(referral)
            db.session.commit()
            
            assert referral.is_overdue is True
            assert referral.days_open == 6
    
    def test_open_referral_exactly_5_days_not_overdue(self, app, test_patient, test_facilities):
        """Open referral exactly 5 days old should NOT be overdue (threshold is >5)"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='open',
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db.session.add(referral)
            db.session.commit()
            
            assert referral.is_overdue is False
            assert referral.days_open == 5
    
    def test_open_referral_under_5_days_not_overdue(self, app, test_patient, test_facilities):
        """Open referral <5 days old should NOT be overdue"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='open',
                created_at=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(referral)
            db.session.commit()
            
            assert referral.is_overdue is False
            assert referral.days_open == 2
    
    def test_arrived_referral_never_overdue(self, app, test_patient, test_facilities):
        """Arrived referral should NEVER be overdue even if >5 days"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='arrived',
                created_at=datetime.utcnow() - timedelta(days=10)
            )
            db.session.add(referral)
            db.session.commit()
            
            assert referral.is_overdue is False
    
    def test_completed_referral_never_overdue(self, app, test_patient, test_facilities):
        """Completed referral should NEVER be overdue even if >5 days"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='completed',
                created_at=datetime.utcnow() - timedelta(days=20)
            )
            db.session.add(referral)
            db.session.commit()
            
            assert referral.is_overdue is False
    
    def test_referral_days_open_calculation(self, app, test_patient, test_facilities):
        """Days open should be correctly calculated"""
        with app.app_context():
            referral = Referral(
                patient_id=test_patient.id,
                from_facility_id=test_facilities[0].id,
                to_facility_id=test_facilities[1].id,
                reason='Test referral',
                status='open',
                created_at=datetime.utcnow() - timedelta(days=8, hours=12)
            )
            db.session.add(referral)
            db.session.commit()
            
            # Should be 8 days (integer division)
            assert referral.days_open == 8
