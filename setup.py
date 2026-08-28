#!/usr/bin/env python
"""Quick setup script to initialize and test MediSight MVP"""

import os
import sys
from app import create_app, db
from app.models import Patient, Facility, Triage, Referral, FollowUp

def main():
    print("🌱 MediSight MVP - Quick Setup\n")
    
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        print("[1/2] Creating database tables...")
        db.create_all()
        print("      ✅ Tables created\n")
        
        # Check if database is empty
        patient_count = Patient.query.count()
        
        if patient_count == 0:
            print("[2/2] Database is empty.")
            print("      Run 'python seed.py' to load demo data.\n")
        else:
            print(f"[2/2] Database already contains {patient_count} patients.")
            print("      (Use 'python seed.py' to reload with fresh demo data)\n")
        
        print("🚀 MediSight MVP is ready!\n")
        print("Quick start:")
        print("  1. Start the app:     python run.py")
        print("  2. Seed demo data:    python seed.py")
        print("  3. Open browser:      http://localhost:5000\n")

if __name__ == '__main__':
    main()
