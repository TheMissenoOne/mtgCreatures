"""
Wrapper for system-wide verification.
Run from project root: python scripts/verify_all_systems.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.analysis.verify_all_systems import verify_all_systems

if __name__ == "__main__":
    verify_all_systems()
