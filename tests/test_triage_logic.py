"""Tests for triage rule-based logic engine"""
import pytest
from app.triage.logic import apply_triage_rules

class TestTriageEmergencyRules:
    """Test emergency escalation rules"""
    
    def test_difficulty_breathing_triggers_emergency(self):
        """Severe difficulty breathing should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Patient having trouble breathing',
            symptom_checkboxes='difficulty_breathing',
            duration_days=1,
            risk_factors=''
        )
        assert outcome_key == 'emergency'
        assert 'Emergency' in outcome_display
    
    def test_chest_pain_triggers_emergency(self):
        """Chest pain should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Severe chest pain',
            symptom_checkboxes='chest_pain',
            duration_days=1,
            risk_factors=''
        )
        assert outcome_key == 'emergency'
    
    def test_unconsciousness_triggers_emergency(self):
        """Unconsciousness should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Patient is unconscious',
            symptom_checkboxes='unconscious',
            duration_days=0,
            risk_factors=''
        )
        assert outcome_key == 'emergency'
    
    def test_severe_bleeding_triggers_emergency(self):
        """Severe bleeding should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='severe_bleeding',
            duration_days=0,
            risk_factors=''
        )
        assert outcome_key == 'emergency'
    
    def test_seizure_triggers_emergency(self):
        """Seizure should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='seizure',
            duration_days=0,
            risk_factors=''
        )
        assert outcome_key == 'emergency'
    
    def test_stroke_symptoms_trigger_emergency(self):
        """Stroke symptoms should trigger Emergency Escalation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='stroke_symptoms',
            duration_days=0,
            risk_factors=''
        )
        assert outcome_key == 'emergency'


class TestTriageInPersonRules:
    """Test 'Needs In-Person Visit' rules"""
    
    def test_pregnant_with_abdominal_pain(self):
        """Pregnant patient with abdominal pain should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Abdominal pain during pregnancy',
            symptom_checkboxes='abdominal_pain',
            duration_days=2,
            risk_factors='pregnancy'
        )
        assert outcome_key == 'in_person'
    
    def test_pregnant_with_long_duration(self):
        """Pregnant patient with symptoms >3 days should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Persistent nausea',
            symptom_checkboxes='vomiting',
            duration_days=5,
            risk_factors='pregnancy'
        )
        assert outcome_key == 'in_person'
    
    def test_elderly_with_multiple_symptoms(self):
        """Elderly patient with 2+ symptoms should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Multiple symptoms',
            symptom_checkboxes='high_fever,persistent_cough',
            duration_days=3,
            risk_factors='elderly'
        )
        assert outcome_key == 'in_person'
    
    def test_chronic_illness_with_multiple_symptoms(self):
        """Chronic illness patient with 2+ symptoms should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='high_fever,severe_headache',
            duration_days=2,
            risk_factors='chronic_illness'
        )
        assert outcome_key == 'in_person'
    
    def test_infant_with_symptoms(self):
        """Infant/young child with any symptoms should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Fever',
            symptom_checkboxes='high_fever',
            duration_days=1,
            risk_factors='infant_young_child'
        )
        assert outcome_key == 'in_person'
    
    def test_long_symptom_duration(self):
        """Symptoms lasting >7 days should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Cough',
            symptom_checkboxes='persistent_cough',
            duration_days=10,
            risk_factors=''
        )
        assert outcome_key == 'in_person'
    
    def test_two_concerning_symptoms(self):
        """Two or more concerning symptoms should need in-person visit"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='high_fever,vomiting',
            duration_days=2,
            risk_factors=''
        )
        assert outcome_key == 'in_person'


class TestTriageTeleconsultRules:
    """Test 'Needs Teleconsultation' rules"""
    
    def test_pregnancy_with_single_symptom(self):
        """Pregnant patient with single symptom should need teleconsultation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Mild nausea',
            symptom_checkboxes='vomiting',
            duration_days=1,
            risk_factors='pregnancy'
        )
        assert outcome_key == 'teleconsult'
    
    def test_chronic_illness_with_single_symptom(self):
        """Chronic illness with single symptom should need teleconsultation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Mild fever',
            symptom_checkboxes='high_fever',
            duration_days=1,
            risk_factors='chronic_illness'
        )
        assert outcome_key == 'teleconsult'
    
    def test_elderly_with_single_symptom(self):
        """Elderly with single symptom should need teleconsultation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Headache',
            symptom_checkboxes='severe_headache',
            duration_days=1,
            risk_factors='elderly'
        )
        assert outcome_key == 'teleconsult'
    
    def test_immunocompromised_with_symptoms(self):
        """Immunocompromised patient with symptoms should need teleconsultation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Mild cough',
            symptom_checkboxes='persistent_cough',
            duration_days=2,
            risk_factors='immunocompromised'
        )
        assert outcome_key == 'teleconsult'
    
    def test_single_symptom_moderate_duration(self):
        """Single symptom >3 days should need teleconsultation"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Sore throat',
            symptom_checkboxes='sore_throat',
            duration_days=4,
            risk_factors=''
        )
        assert outcome_key == 'teleconsult'


class TestTriageRoutineRules:
    """Test 'Routine' outcome rules"""
    
    def test_mild_cold_no_risk_factors(self):
        """Mild cold with no risk factors should be routine"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Runny nose',
            symptom_checkboxes='runny_nose',
            duration_days=1,
            risk_factors=''
        )
        assert outcome_key == 'routine'
    
    def test_no_symptoms_no_risk_factors(self):
        """No symptoms and no risk factors should be routine"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='',
            duration_days=0,
            risk_factors=''
        )
        assert outcome_key == 'routine'
    
    def test_single_mild_symptom_short_duration(self):
        """Single mild symptom <3 days should be routine"""
        outcome_key, outcome_display = apply_triage_rules(
            symptoms_text='Stuffy nose',
            symptom_checkboxes='runny_nose',
            duration_days=2,
            risk_factors=''
        )
        assert outcome_key == 'routine'


class TestTriagePriorityOrder:
    """Test that rules follow correct priority order"""
    
    def test_emergency_overrides_all(self):
        """Emergency flags should override risk factors"""
        outcome_key, _ = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='chest_pain',  # Emergency
            duration_days=1,
            risk_factors='pregnancy'  # Would normally be in-person
        )
        assert outcome_key == 'emergency'
    
    def test_in_person_overrides_teleconsult(self):
        """In-person should override teleconsult rules"""
        outcome_key, _ = apply_triage_rules(
            symptoms_text='',
            symptom_checkboxes='high_fever,persistent_cough',  # 2 symptoms = in-person
            duration_days=2,
            risk_factors='pregnancy'  # Also has pregnancy risk
        )
        assert outcome_key == 'in_person'
