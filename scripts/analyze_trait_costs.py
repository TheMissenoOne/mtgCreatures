"""
Wrapper for trait cost analysis.
Run from project root: python scripts/analyze_trait_costs.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.analysis.analyze_trait_costs import analyze_trait_costs

if __name__ == "__main__":
    analyze_trait_costs()
