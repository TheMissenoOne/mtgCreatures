"""
Wrapper entry point for MTG to D&D conversion pipeline.
Delegates to the backend conversion module.
"""

import sys
from pathlib import Path

# Add backend to path so imports work
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Now import and run main
from main import main

if __name__ == "__main__":
    main()
