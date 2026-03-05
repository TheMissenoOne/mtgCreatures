"""
Wrapper for defensive budget analysis.
Run from project root: python -m backend.analysis.analyze_defensive_budgets
or: python scripts/analyze_defensive_budgets.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.analysis.analyze_defensive_budgets import analyze_defensive_budgets

if __name__ == "__main__":
    analyze_defensive_budgets()
