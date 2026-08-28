"""Triage rule engine for deterministic risk assessment"""

def apply_triage_rules(symptoms_text, symptom_checkboxes, duration_days, risk_factors):
    """
    Apply rule-based triage logic to determine patient priority.
    
    Args:
        symptoms_text: Free-text symptom description
        symptom_checkboxes: CSV string of selected symptom checkboxes
        duration_days: How many days symptoms have persisted
        risk_factors: CSV string of selected risk factors
    
    Returns:
        tuple: (outcome_key, outcome_display_name)
        outcome_key: 'emergency', 'in_person', 'teleconsult', 'routine'
    """
    
    # Parse CSV inputs
    symptoms = set(s.strip() for s in (symptom_checkboxes or '').split(',') if s.strip())
    risks = set(r.strip() for r in (risk_factors or '').split(',') if r.strip())
    
    # PRIORITY 1: Emergency Red Flags
    emergency_flags = {
        'difficulty_breathing',
        'chest_pain',
        'unconscious',
        'confusion',
        'severe_bleeding',
        'seizure',
        'stroke_symptoms'
    }
    
    if symptoms & emergency_flags:
        return ('emergency', 'Emergency Escalation')
    
    # PRIORITY 2: High-Risk Situations requiring In-Person Visit
    
    # Pregnant patients with concerning symptoms or duration
    if 'pregnancy' in risks:
        if 'abdominal_pain' in symptoms or 'vaginal_bleeding' in symptoms:
            return ('in_person', 'Needs In-Person Visit')
        if duration_days and duration_days > 3:
            return ('in_person', 'Needs In-Person Visit')
    
    # Elderly or chronic illness with multiple symptoms
    if ('elderly' in risks or 'chronic_illness' in risks):
        symptom_count = len(symptoms)
        if symptom_count >= 2:
            return ('in_person', 'Needs In-Person Visit')
    
    # Infant/young child with symptoms
    if 'infant_young_child' in risks and len(symptoms) > 0:
        return ('in_person', 'Needs In-Person Visit')
    
    # Long duration of symptoms
    if duration_days and duration_days > 7:
        return ('in_person', 'Needs In-Person Visit')
    
    # Multiple concerning symptoms
    concerning_symptoms = {
        'high_fever',
        'persistent_cough',
        'severe_headache',
        'vomiting',
        'diarrhea',
        'abdominal_pain'
    }
    if len(symptoms & concerning_symptoms) >= 2:
        return ('in_person', 'Needs In-Person Visit')
    
    # PRIORITY 3: High-Risk Factors with Non-Emergency Symptoms → Teleconsultation
    
    if ('pregnancy' in risks or 'chronic_illness' in risks or 
        'elderly' in risks or 'immunocompromised' in risks):
        if len(symptoms) > 0 or (duration_days and duration_days > 0):
            return ('teleconsult', 'Needs Teleconsultation')
    
    # Single symptom with moderate duration
    if len(symptoms) == 1 and duration_days and duration_days > 3:
        return ('teleconsult', 'Needs Teleconsultation')
    
    # PRIORITY 4: Routine
    return ('routine', 'Routine')


def get_emergency_flags():
    """Return list of emergency symptom flags for form rendering"""
    return [
        ('difficulty_breathing', 'Severe Difficulty Breathing'),
        ('chest_pain', 'Chest Pain'),
        ('unconscious', 'Unconsciousness'),
        ('confusion', 'Confusion/Altered Mental State'),
        ('severe_bleeding', 'Severe Bleeding'),
        ('seizure', 'Seizure'),
        ('stroke_symptoms', 'Stroke-like Symptoms')
    ]


def get_common_symptoms():
    """Return list of common symptoms for form rendering"""
    return [
        ('high_fever', 'High Fever (>39°C)'),
        ('persistent_cough', 'Persistent Cough'),
        ('sore_throat', 'Sore Throat'),
        ('runny_nose', 'Runny/Stuffy Nose'),
        ('severe_headache', 'Severe Headache'),
        ('body_aches', 'Body Aches'),
        ('vomiting', 'Vomiting'),
        ('diarrhea', 'Diarrhea'),
        ('abdominal_pain', 'Abdominal Pain'),
        ('vaginal_bleeding', 'Vaginal Bleeding'),
        ('weakness', 'Unusual Weakness/Fatigue'),
        ('rash', 'Skin Rash')
    ]


def get_risk_factors():
    """Return list of risk factors for form rendering"""
    return [
        ('pregnancy', 'Pregnancy'),
        ('chronic_illness', 'Chronic Illness (diabetes, hypertension, etc.)'),
        ('elderly', 'Elderly (>65 years)'),
        ('infant_young_child', 'Infant or Young Child (<5 years)'),
        ('immunocompromised', 'Immunocompromised')
    ]
