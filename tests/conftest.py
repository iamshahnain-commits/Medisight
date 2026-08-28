# Testing configuration for MediSight MVP
import pytest
from app import create_app, db
from app.models import Patient, Facility, Triage, Referral, FollowUp

@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def test_patient(app):
    """Create a test patient"""
    with app.app_context():
        patient = Patient(
            patient_id='TEST001',
            name='Test Patient',
            age=30,
            gender='M'
        )
        db.session.add(patient)
        db.session.commit()
        return patient

@pytest.fixture
def test_facilities(app):
    """Create test facilities"""
    with app.app_context():
        fac1 = Facility(
            code='FAC001',
            name='Test Facility 1',
            facility_type='PHC'
        )
        fac2 = Facility(
            code='FAC002',
            name='Test Facility 2',
            facility_type='Hospital'
        )
        db.session.add_all([fac1, fac2])
        db.session.commit()
        return [fac1, fac2]
