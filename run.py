#!/usr/bin/env python
"""MediSight MVP Flask Application Entry Point"""

from app import create_app, db
from app.models import Patient, Facility, Triage, Referral, FollowUp

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    """Make models available in Flask shell"""
    return {
        'db': db,
        'Patient': Patient,
        'Facility': Facility,
        'Triage': Triage,
        'Referral': Referral,
        'FollowUp': FollowUp
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
