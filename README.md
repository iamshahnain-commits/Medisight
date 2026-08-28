# MediSight MVP - Hospital Management & Continuity System

**MediSight MVP** is a Flask-based hospital management system designed for Government of Maharashtra's hackathon (Problem Statement 26133: improving accessibility, continuity and quality of public healthcare in rural/underserved areas). This MVP extends the facility-level core with a continuity layer: **digital triage, trackable referrals, and a high-risk follow-up queue**.

## ✨ Features

### 1. Digital Triage Assessment
- Simple, rule-based triage form for rapid patient risk categorization
- Free-text symptom description + checkbox selection for red-flag symptoms
- Risk factor multi-select (pregnancy, chronic illness, elderly, etc.)
- Symptom duration tracking
- **Automatic triage outcomes**: Routine → Teleconsultation → In-Person Visit → Emergency Escalation
- Transparent, deterministic rule engine (no ML/black-box)
- Automatic follow-up creation for high-risk cases

### 2. Referral Tracking
- Create and manage referrals between facilities
- Track referral status: Open → Arrived → Completed
- **Automatic overdue detection**: Referrals open > 5 days flagged as overdue
- Facility-to-facility traceability
- Configurable overdue threshold (default: 5 days)

### 3. High-Risk Follow-Up Queue
- Automatic follow-up creation for high-risk triage cases and completed referrals
- Follow-up due date scheduling (default: +7 days)
- Duplicate prevention logic
- **Quick filtering**: Due today / Upcoming
- Mark follow-ups as completed

### 4. Admin Dashboard
- **Key metrics**: Total patients, open referrals, overdue referrals, follow-ups due today
- Overdue referrals table with detailed information
- Follow-ups due today with quick actions
- Real-time computation (no background jobs required)

## 🏗️ Project Structure

```
MediSight/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # SQLAlchemy models (Patient, Facility, Triage, Referral, FollowUp)
│   ├── utils.py                    # Helper functions (overdue calculation, follow-up creation)
│   ├── main/
│   │   └── routes.py               # Home and patient listing routes
│   ├── patients/
│   │   └── routes.py               # Patient registration, edit
│   ├── triage/
│   │   ├── __init__.py             # Triage rule engine logic
│   │   └── routes.py               # Triage form, assessment, results
│   ├── referrals/
│   │   └── routes.py               # Referral CRUD and status updates
│   ├── followups/
│   │   └── routes.py               # Follow-up queue and completion
│   ├── dashboard/
│   │   └── routes.py               # Admin dashboard with metrics
│   └── templates/                  # Jinja2 HTML templates (Bootstrap 5)
│       ├── base.html               # Base template with navigation
│       ├── dashboard/
│       ├── patients/
│       ├── triage/
│       ├── referrals/
│       └── followups/
├── tests/
│   ├── conftest.py                 # Pytest fixtures and test config
│   ├── test_triage_logic.py        # Triage rule engine tests
│   └── test_referrals.py           # Referral overdue calculation tests
├── config.py                       # Flask configuration (dev, test, prod)
├── run.py                          # Application entry point
├── seed.py                         # Database seed script with demo data
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🗄️ Database Models

### Patient
- `patient_id` (unique, indexed)
- `name`, `age`, `gender`, `phone`, `address`
- Relationships: triages, referrals, followups

### Facility
- `code` (unique), `name`, `location`, `facility_type` (PHC, Hospital, Sub-center, etc.)
- `phone`
- Relationships: referrals (from/to)

### Triage
- `patient_id` (FK)
- `symptoms` (free-text), `symptom_checkboxes` (CSV)
- `duration_days`, `risk_factors` (CSV)
- `triage_result` + `triage_result_display` (outcome)
- `created_at` (indexed)

### Referral
- `patient_id`, `from_facility_id`, `to_facility_id` (FKs, indexed)
- `reason`, `status` ('open' | 'arrived' | 'completed')
- `created_at`, `updated_at` (indexed)
- **Computed property**: `is_overdue` (status='open' AND age > 5 days)

### FollowUp
- `patient_id` (FK, indexed)
- `reason`, `scheduled_date` (indexed), `status` ('pending' | 'completed')
- `created_at`, `completed_at`
- **Computed property**: `is_due_today` (status='pending' AND scheduled_date <= today)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/iamshahnain-commits/Medisight.git
   cd Medisight
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database** (creates SQLite in `instance/medisight.db`)
   ```bash
   python run.py
   ```
   The app will start on `http://localhost:5000`. Stop it (Ctrl+C).

5. **Seed the database with demo data** (optional but recommended)
   ```bash
   python seed.py
   ```
   This creates:
   - 5 patients
   - 4 facilities (PHC, Sub-center, Hospital)
   - 5 triage records (mix of outcomes)
   - 5 referrals (some open, some overdue, some completed)
   - 5 follow-ups (some due today, some upcoming, some completed)

   **Note**: The dashboard will be empty until you run this!

## ▶️ Running the Application

```bash
# Start the Flask development server
python run.py
```

Then open your browser to: **http://localhost:5000**

**Navigation:**
- 📊 Dashboard — Key metrics and overdue referrals
- 👥 Patients — List, register, view patient records
- 📋 Triage — Perform digital triage assessments
- ↔️ Referrals — Create and manage referrals between facilities
- 📝 Follow-ups — Follow-up queue (due today/upcoming)

## 🧪 Running Tests

The project includes comprehensive pytest tests for:
- **Triage rule logic**: Emergency escalation, in-person visits, teleconsultation, routine
- **Referral overdue calculation**: Edge cases around the 5-day threshold

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_triage_logic.py -v
pytest tests/test_referrals.py -v

# Run with coverage
pytest --cov=app --cov=tests
```

### Test Coverage

**test_triage_logic.py** (~30 tests):
- Emergency red flags (6 tests): chest pain, difficulty breathing, unconsciousness, severe bleeding, seizure, stroke
- In-person rules (7 tests): pregnancy, elderly, chronic illness, long duration, multiple symptoms
- Teleconsultation rules (5 tests): high-risk factors with mild symptoms
- Routine rules (3 tests): no symptoms, mild symptoms, low risk
- Priority order (3 tests): emergency overrides all, in-person overrides teleconsult

**test_referrals.py** (~5 tests):
- Overdue calculation: >5 days, =5 days, <5 days
- Status impact: arrived/completed never overdue
- Days open calculation

## 📊 Triage Rule Engine

The rule-based triage logic is fully transparent and deterministic:

### Priority 1: Emergency Escalation
Any of these symptoms → **IMMEDIATE ACTION REQUIRED**
- Severe difficulty breathing
- Chest pain
- Unconsciousness/confusion
- Severe bleeding
- Seizure
- Stroke-like symptoms

### Priority 2: Needs In-Person Visit
- Pregnant patients with concerning symptoms (abdominal pain, vaginal bleeding) or duration > 3 days
- Elderly or chronic illness patients with 2+ symptoms
- Infant/young child with any symptoms
- Symptoms lasting > 7 days
- 2+ concerning symptoms (fever, persistent cough, severe headache, vomiting, diarrhea, abdominal pain)

### Priority 3: Needs Teleconsultation
- High-risk factors (pregnancy, chronic illness, elderly, immunocompromised) with non-emergency symptoms
- Single symptom lasting > 3 days

### Priority 4: Routine
- No emergency flags, no concerning combinations
- Can be managed with basic care

## 🔧 Configuration

Edit `config.py` to customize:

```python
REFERRAL_OVERDUE_DAYS = 5        # Days before a referral is marked overdue
FOLLOWUP_SUGGESTED_DAYS = 7      # Default days offset for follow-up scheduling
```

Environment variables:
- `FLASK_ENV` — 'development' | 'production'
- `SECRET_KEY` — Flask secret key (auto-generated if not set)

## 📝 Example Workflows

### Workflow 1: Triage & Auto Follow-up
1. Open **Triage** form
2. Select patient, enter symptoms, select red flags/risk factors
3. Submit → Triage result displayed
4. If high-risk: Follow-up automatically created (due in 7 days)
5. Follow-up appears in **Follow-ups** queue

### Workflow 2: Create Referral
1. Open **Referrals** → **Create Referral**
2. Select patient, from facility, to facility, reason
3. Referral created with status 'open'
4. Admin updates status as patient progresses (arrived → completed)
5. When marked 'completed': Follow-up auto-created for patient

### Workflow 3: Monitor Overdue Referrals
1. Dashboard shows **Overdue Referrals** count
2. Click through to see detailed table
3. View individual referral to update status
4. Once status changes from 'open': No longer overdue

## 🚫 MVP Limitations (Out of Scope)

This MVP deliberately excludes:
- **Teleconsultation** — No video/call implementation; just workflow flags
- **Offline sync** — No sync layer; requires internet
- **Multilingual UI** — English only for MVP
- **Interoperability layer** — No integration with other systems
- **ML-based triage** — Rule-based only (transparent, hackathon-appropriate)
- **Background jobs** — All calculations synchronous, at query time
- **Advanced charting** — Simple HTML tables/cards only
- **Real authentication** — No login/roles; single-user MVP

## 🛠️ Development Notes

### Adding a New Route
1. Create a blueprint in `app/feature/routes.py`
2. Register in `app/__init__.py`
3. Create templates in `app/templates/feature/`
4. Add tests in `tests/`

### Database Migrations
For now, the app auto-creates tables on startup. For production, consider Flask-Migrate.

### Testing New Logic
```bash
# Enter Flask shell
python -m flask --app run shell

# Query models
>>> from app.models import *
>>> Patient.query.all()
>>> Referral.query.filter_by(status='open').all()
```

## 📞 Support & Contact

Built for Maharashtra Healthcare Hackathon 2026 — Problem Statement 26133.

## 📄 License

Open source for hackathon purposes.

---

**Happy hacking!** 🏥💻
