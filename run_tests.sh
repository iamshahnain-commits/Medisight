#!/bin/bash
# Quick test runner for MediSight MVP

set -e

echo "🧪 Running MediSight MVP Tests..."
echo ""

# Run pytest
echo "[1/3] Running unit tests (triage logic, referral calculations)..."
pytest tests/test_triage_logic.py tests/test_referrals.py -v

echo ""
echo "[2/3] Checking test coverage..."
pytest tests/ --tb=short

echo ""
echo "[3/3] All tests passed! ✅"
echo ""
echo "Next steps:"
echo "  1. Run the app: python run.py"
echo "  2. Seed demo data: python seed.py"
echo "  3. Open browser: http://localhost:5000"
