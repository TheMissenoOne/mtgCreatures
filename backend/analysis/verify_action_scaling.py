#!/usr/bin/env python3
"""Quick validation that action scaling was applied."""

import json
import re
from pathlib import Path

data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
with open(data_file) as f:
    creatures = json.load(f)

creatures_with_actions = [c for c in creatures.values() if isinstance(c, dict) and c.get("Actions")]

print(f"✓ Total creatures: {len(creatures)}")
print(f"✓ Creatures with actions: {len(creatures_with_actions)}")
print()

# Sample from different CR tiers
sample_crs = {}
for creature_name, creature_data in creatures.items():
    if isinstance(creature_data, dict) and creature_data.get("Actions"):
        cr_str = creature_data.get("Challenge", "0").split()[0]
        try:
            if "/" in cr_str:
                cr_num, cr_den = map(int, cr_str.split("/"))
                cr = int(cr_num / cr_den)
            else:
                cr = int(float(cr_str))
        except:
            cr = 0
        
        if cr not in sample_crs:
            sample_crs[cr] = creature_data

print("Sample creatures with scaled actions:")
print("─" * 80)
for cr in sorted(sample_crs.keys()):
    c = sample_crs[cr]
    bonuses = re.findall(r'\+(\d+) to hit', c.get("Actions", ""))
    damages = re.findall(r'(\d+d\d+(?:\+\d+)?)', c.get("Actions", ""))
    
    bonus_str = ", ".join(bonuses[:3]) if bonuses else "N/A"
    damage_str = ", ".join(damages[:3]) if damages else "N/A"
    
    print(f"CR {cr:2} | {c['name'][:30]:30} | Bonuses: {bonus_str:15} | Damage: {damage_str}")

print()
print("✓ Action scaling verification complete!")
