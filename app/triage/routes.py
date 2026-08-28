from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Patient, Triage
from app.triage import logic
from app.utils import create_followup_for_patient
from datetime import datetime

triage_bp = Blueprint('triage', __name__, url_prefix='/triage')

@triage_bp.route('/form', methods=['GET', 'POST'])
def form():
    """Display triage form or handle submission"""
    patients = Patient.query.all()
    emergency_flags = logic.get_emergency_flags()
    common_symptoms = logic.get_common_symptoms()
    risk_factors = logic.get_risk_factors()
    
    if request.method == 'POST':
        patient_id = request.form.get('patient_id', type=int)
        symptoms_text = request.form.get('symptoms_text', '').strip()
        symptom_checkboxes = ','.join(request.form.getlist('symptoms'))
        duration_days = request.form.get('duration_days', type=int)
        risk_factor_list = ','.join(request.form.getlist('risk_factors'))
        
        # Validate patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            flash('Invalid patient selected', 'danger')
            return redirect(url_for('triage.form'))
        
        # Apply triage logic
        outcome_key, outcome_display = logic.apply_triage_rules(
            symptoms_text,
            symptom_checkboxes,
            duration_days,
            risk_factor_list
        )
        
        # Create triage record
        triage = Triage(
            patient_id=patient_id,
            symptoms=symptoms_text,
            symptom_checkboxes=symptom_checkboxes,
            duration_days=duration_days,
            risk_factors=risk_factor_list,
            triage_result=outcome_key,
            triage_result_display=outcome_display
        )
        db.session.add(triage)
        db.session.commit()
        
        # Auto-create follow-up for high-risk cases
        if outcome_key in ['emergency', 'in_person']:
            create_followup_for_patient(
                patient_id,
                f'High-risk triage: {outcome_display}',
                offset_days=7
            )
        
        flash('Triage assessment completed', 'success')
        return redirect(url_for('triage.result', triage_id=triage.id))
    
    return render_template('triage/form.html',
                         patients=patients,
                         emergency_flags=emergency_flags,
                         common_symptoms=common_symptoms,
                         risk_factors=risk_factors)


@triage_bp.route('/result/<int:triage_id>')
def result(triage_id):
    """Display triage result"""
    triage = Triage.query.get_or_404(triage_id)
    return render_template('triage/result.html', triage=triage)


@triage_bp.route('/history/<int:patient_id>')
def history(patient_id):
    """View triage history for a patient"""
    patient = Patient.query.get_or_404(patient_id)
    triages = Triage.query.filter_by(patient_id=patient_id).order_by(Triage.created_at.desc()).all()
    return render_template('triage/history.html', patient=patient, triages=triages)
