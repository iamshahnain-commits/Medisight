import os
import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Patient, Facility, Triage, Referral, FollowUp

def seed_database():
    """Seed the database with realistic demo data"""
    
    # Clear existing data
    db.session.query(FollowUp).delete()
    db.session.query(Triage).delete()
    db.session.query(Referral).delete()
    db.session.query(Patient).delete()
    db.session.query(Facility).delete()
    db.session.commit()
    
    print("🌱 Seeding MediSight database...")
    
    # Create Facilities
    print("  → Creating facilities...")
    phc_village_a = Facility(
        code='PHC001',
        name='Village A Primary Health Center',
        location='Village A, Block 1',
        facility_type='PHC',
        phone='9876543210'
    )
    phc_village_b = Facility(
        code='PHC002',
        name='Village B Primary Health Center',
        location='Village B, Block 2',
        facility_type='PHC',
        phone='9876543211'
    )
    subcenter_hamlet_c = Facility(
        code='SC001',
        name='Hamlet C Sub-center',
        location='Hamlet C, Block 1',
        facility_type='Sub-center',
        phone='9876543212'
    )
    district_hospital = Facility(
        code='DH001',
        name='District General Hospital',
        location='District Town',
        facility_type='Hospital',
        phone='9876543213'
    )
    
    db.session.add_all([phc_village_a, phc_village_b, subcenter_hamlet_c, district_hospital])
    db.session.commit()
    
    # Create Patients
    print("  → Creating patients...")
    patient1 = Patient(
        patient_id='P001',
        name='Ramesh Kumar',
        age=45,
        gender='M',
        phone='9876543220',
        address='House 12, Village A'
    )
    patient2 = Patient(
        patient_id='P002',
        name='Priya Sharma',
        age=32,
        gender='F',
        phone='9876543221',
        address='House 5, Village B'
    )
    patient3 = Patient(
        patient_id='P003',
        name='Rajesh Patel',
        age=72,
        gender='M',
        phone='9876543222',
        address='House 8, Hamlet C'
    )
    patient4 = Patient(
        patient_id='P004',
        name='Sneha Desai',
        age=28,
        gender='F',
        phone='9876543223',
        address='House 15, Village A'
    )
    patient5 = Patient(
        patient_id='P005',
        name='Vikram Singh',
        age=55,
        gender='M',
        phone='9876543224',
        address='House 20, Village B'
    )
    
    db.session.add_all([patient1, patient2, patient3, patient4, patient5])
    db.session.commit()
    
    # Create Triages
    print("  → Creating triage records...")
    triage1 = Triage(
        patient_id=patient1.id,
        symptoms='High fever and severe cough for past 2 weeks',
        symptom_checkboxes='high_fever,persistent_cough',
        duration_days=14,
        risk_factors='chronic_illness',
        triage_result='in_person',
        triage_result_display='Needs In-Person Visit'
    )
    triage2 = Triage(
        patient_id=patient2.id,
        symptoms='Mild cold and runny nose',
        symptom_checkboxes='runny_nose',
        duration_days=2,
        risk_factors='',
        triage_result='routine',
        triage_result_display='Routine'
    )
    triage3 = Triage(
        patient_id=patient3.id,
        symptoms='Severe chest pain and difficulty breathing',
        symptom_checkboxes='chest_pain,difficulty_breathing',
        duration_days=1,
        risk_factors='elderly,chronic_illness',
        triage_result='emergency',
        triage_result_display='Emergency Escalation'
    )
    triage4 = Triage(
        patient_id=patient4.id,
        symptoms='Abdominal pain with nausea, possibly pregnant',
        symptom_checkboxes='abdominal_pain,vomiting',
        duration_days=3,
        risk_factors='pregnancy',
        triage_result='in_person',
        triage_result_display='Needs In-Person Visit'
    )
    triage5 = Triage(
        patient_id=patient5.id,
        symptoms='Persistent headache and body aches',
        symptom_checkboxes='severe_headache,body_aches',
        duration_days=5,
        risk_factors='',
        triage_result='teleconsult',
        triage_result_display='Needs Teleconsultation'
    )
    
    db.session.add_all([triage1, triage2, triage3, triage4, triage5])
    db.session.commit()
    
    # Create Referrals
    print("  → Creating referrals...")
    
    # Open referral - recent
    referral1 = Referral(
        patient_id=patient1.id,
        from_facility_id=phc_village_a.id,
        to_facility_id=district_hospital.id,
        reason='Chronic illness with complications requiring specialist evaluation',
        status='open',
        created_at=datetime.utcnow() - timedelta(days=2)
    )
    
    # Open referral - OVERDUE
    referral2 = Referral(
        patient_id=patient3.id,
        from_facility_id=subcenter_hamlet_c.id,
        to_facility_id=district_hospital.id,
        reason='Emergency: Acute cardiac symptoms, possible MI',
        status='open',
        created_at=datetime.utcnow() - timedelta(days=7)
    )
    
    # Open referral - just at threshold
    referral3 = Referral(
        patient_id=patient4.id,
        from_facility_id=phc_village_b.id,
        to_facility_id=district_hospital.id,
        reason='Pregnancy complications: abdominal pain and vaginal bleeding',
        status='open',
        created_at=datetime.utcnow() - timedelta(days=5)
    )
    
    # Arrived referral
    referral4 = Referral(
        patient_id=patient2.id,
        from_facility_id=phc_village_a.id,
        to_facility_id=phc_village_b.id,
        reason='Routine follow-up consultation',
        status='arrived',
        created_at=datetime.utcnow() - timedelta(days=3)
    )
    
    # Completed referral
    referral5 = Referral(
        patient_id=patient5.id,
        from_facility_id=phc_village_b.id,
        to_facility_id=district_hospital.id,
        reason='Specialist consultation for persistent headaches',
        status='completed',
        created_at=datetime.utcnow() - timedelta(days=10),
        updated_at=datetime.utcnow() - timedelta(days=3)
    )
    
    db.session.add_all([referral1, referral2, referral3, referral4, referral5])
    db.session.commit()
    
    # Create Follow-ups
    print("  → Creating follow-up records...")
    
    # Follow-up due today
    followup1 = FollowUp(
        patient_id=patient1.id,
        reason='High-risk triage: Needs In-Person Visit',
        scheduled_date=datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
        status='pending'
    )
    
    # Follow-up OVERDUE
    followup2 = FollowUp(
        patient_id=patient3.id,
        reason='Follow-up: Referral to District General Hospital completed',
        scheduled_date=datetime.utcnow() - timedelta(days=2),
        status='pending'
    )
    
    # Follow-up upcoming
    followup3 = FollowUp(
        patient_id=patient4.id,
        reason='High-risk triage: Needs In-Person Visit',
        scheduled_date=datetime.utcnow() + timedelta(days=3),
        status='pending'
    )
    
    # Follow-up upcoming
    followup4 = FollowUp(
        patient_id=patient5.id,
        reason='Follow-up: Referral to District General Hospital completed',
        scheduled_date=datetime.utcnow() + timedelta(days=5),
        status='pending'
    )
    
    # Completed follow-up
    followup5 = FollowUp(
        patient_id=patient2.id,
        reason='Routine check-in',
        scheduled_date=datetime.utcnow() - timedelta(days=3),
        status='completed',
        completed_at=datetime.utcnow() - timedelta(days=2)
    )
    
    db.session.add_all([followup1, followup2, followup3, followup4, followup5])
    db.session.commit()
    
    print("\n✅ Database seeding completed successfully!")
    print(f"   Created: 5 Patients, 4 Facilities, 5 Triages, 5 Referrals, 5 Follow-ups")
    print(f"\n📊 Dashboard should now show:")
    print(f"   - 1 overdue referral (7 days old)")
    print(f"   - 1-2 follow-ups due today")
    print(f"   - Mix of routine and high-risk triage cases")

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        seed_database()
