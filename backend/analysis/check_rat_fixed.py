#!/usr/bin/env python3
"""Check if Burglar Rat was fixed by defensive budgeting."""

import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
with open(data_file) as f:
    creatures = json.load(f)

# Search for Burglar Rat
rat = None
for name, data in creatures.items():
    if "Burglar Rat" in name or "burglar rat" in name.lower():
        rat = data
        print(f"Found: {name}")
        break

if rat:
    print(f"Challenge: {rat.get('Challenge', 'N/A')}")
    print(f"AC: {rat.get('Armor Class', 'N/A')}")
    print(f"HP: {rat.get('Hit Points', 'N/A')}")
    
    # Parse CR
    cr_str = rat.get('Challenge', '0').split()[0]
    try:
        if '/' in cr_str:
            cr_num, cr_den = map(int, cr_str.split('/'))
            cr = cr_num / cr_den
        else:
            cr = float(cr_str)
    except:
        cr = 0
    
    print(f"CR: {cr}")
    
    # Check budgets
    from stats_calculator import get_ac_budget, get_hp_budget
    ac_budget = get_ac_budget(cr)
    hp_budget = get_hp_budget(cr)
    
    print(f"AC Budget for CR {cr}: {ac_budget[0]}-{ac_budget[1]}")
    print(f"HP Budget for CR {cr}: {hp_budget[0]}-{hp_budget[1]}")
    
    ac_val = int(rat.get('Armor Class', 10)) if isinstance(rat.get('Armor Class'), int) else int(rat.get('Armor Class', '10').split()[0])
    hp_val = int(rat.get('Hit Points', 10)) if isinstance(rat.get('Hit Points'), int) else int(rat.get('Hit Points', '10').split()[0])
    
    print(f"\n✓ AC {ac_val} is within budget: {ac_budget[0] <= ac_val <= ac_budget[1]}")
    print(f"✓ HP {hp_val} is within budget: {hp_budget[0] <= hp_val <= hp_budget[1]}")
    
    if ac_val <= ac_budget[1] and hp_val <= hp_budget[1]:
        print("\n✅ Burglar Rat is now properly balanced!")
    else:
        print("\n❌ Burglar Rat still exceeds budget")
else:
    print("Burglar Rat not found in creatures")
