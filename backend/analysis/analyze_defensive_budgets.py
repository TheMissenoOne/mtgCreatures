#!/usr/bin/env python3
"""
Analyze defensive stat budgeting to ensure AC and HP match CR.
Shows that low-CR creatures are no longer overpowered defensively.
"""

import json
from collections import defaultdict
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from stats_calculator import get_ac_budget, get_hp_budget

def analyze_defensive_budgets():
    """Analyze AC and HP distribution by CR tier."""
    data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
    with open(data_file) as f:
        creatures = json.load(f)
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     DEFENSIVE STAT BUDGET ANALYSIS - CR-BASED VALIDATION        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    cr_data = defaultdict(list)
    violations = []
    
    for creature_name, creature_data in creatures.items():
        if isinstance(creature_data, dict):
            cr_str = creature_data.get("Challenge", "0")
            
            try:
                cr_str = cr_str.split()[0]
                if "/" in cr_str:
                    cr_num, cr_den = map(int, cr_str.split("/"))
                    cr = cr_num / cr_den
                else:
                    cr = float(cr_str)
            except (ValueError, ZeroDivisionError, AttributeError, IndexError):
                cr = 0
            
            # Parse AC and HP
            ac = creature_data.get("Armor Class")
            hp = creature_data.get("Hit Points")
            
            if isinstance(ac, str):
                ac = int(ac.split()[0])
            if isinstance(hp, str):
                hp = int(hp.split()[0])
            
            ac_budget = get_ac_budget(cr)
            hp_budget = get_hp_budget(cr)
            
            cr_data[cr].append({
                "name": creature_name,
                "ac": ac,
                "hp": hp,
                "ac_budget": ac_budget,
                "hp_budget": hp_budget
            })
            
            # Check for violations
            if ac is not None and (ac < ac_budget[0] or ac > ac_budget[1]):
                violations.append({
                    "name": creature_name,
                    "type": "AC",
                    "cr": cr,
                    "value": ac,
                    "budget": ac_budget
                })
            
            if hp is not None and hp < hp_budget[0]:
                violations.append({
                    "name": creature_name,
                    "type": "HP_LOW",
                    "cr": cr,
                    "value": hp,
                    "budget": hp_budget
                })
            elif hp is not None and hp > hp_budget[1]:
                violations.append({
                    "name": creature_name,
                    "type": "HP_HIGH",
                    "cr": cr,
                    "value": hp,
                    "budget": hp_budget
                })
    
    # Print summary by CR
    print("CR    | Creatures | Avg AC  | AC Range | Avg HP  | HP Range")
    print("─" * 70)
    
    for cr in sorted(cr_data.keys()):
        data_list = cr_data[cr]
        if not data_list:
            continue
        
        acs = [d["ac"] for d in data_list if d["ac"] is not None]
        hps = [d["hp"] for d in data_list if d["hp"] is not None]
        
        avg_ac = sum(acs) / len(acs) if acs else 0
        min_ac = min(acs) if acs else 0
        max_ac = max(acs) if acs else 0
        
        avg_hp = sum(hps) / len(hps) if hps else 0
        min_hp = min(hps) if hps else 0
        max_hp = max(hps) if hps else 0
        
        cr_display = f"{cr:.1f}" if cr % 1 != 0 else f"{int(cr)}"
        print(f"CR {cr_display:3} | {len(data_list):9} | {avg_ac:7.1f} | {min_ac:2}-{max_ac:2}    | {avg_hp:7.1f} | {min_hp:3}-{max_hp:3}")
    
    print()
    print("BUDGET COMPLIANCE SUMMARY")
    print("─" * 70)
    
    total = len(creatures)
    violation_count = len(violations)
    compliance_rate = ((total - violation_count) / total * 100) if total > 0 else 0
    
    print(f"Total creatures: {total}")
    print(f"Defensive violations: {violation_count} ({100 - compliance_rate:.1f}%)")
    print(f"Budget compliance rate: {compliance_rate:.1f}%")
    print()
    
    # Categorize violations
    if violations:
        ac_violations = [v for v in violations if v["type"] == "AC"]
        hp_high_violations = [v for v in violations if v["type"] == "HP_HIGH"]
        hp_low_violations = [v for v in violations if v["type"] == "HP_LOW"]
        
        print("VIOLATION DETAILS")
        print("─" * 70)
        if ac_violations:
            print(f"AC out of budget: {len(ac_violations)}")
            for v in ac_violations[:5]:
                print(f"  {v['name'][:30]:30} CR {v['cr']:5.1f} | AC {v['value']:2} (budget: {v['budget'][0]}-{v['budget'][1]})")
        
        if hp_high_violations:
            print(f"HP too high: {len(hp_high_violations)}")
            for v in hp_high_violations[:5]:
                print(f"  {v['name'][:30]:30} CR {v['cr']:5.1f} | HP {v['value']:3} (budget: {v['budget'][0]}-{v['budget'][1]})")
        
        if hp_low_violations:
            print(f"HP too low: {len(hp_low_violations)}")
            for v in hp_low_violations[:5]:
                print(f"  {v['name'][:30]:30} CR {v['cr']:5.1f} | HP {v['value']:3} (budget: {v['budget'][0]}-{v['budget'][1]})")
    else:
        print("✅ All creatures have AC and HP within budget!")
    
    print()
    print("SAMPLE CREATURES BY CR")
    print("─" * 70)
    
    sample_crs = [0.25, 1, 2, 4, 6, 8, 10, 15, 20]
    for target_cr in sample_crs:
        matches = []
        for cr in cr_data:
            if abs(cr - target_cr) < 0.6:
                matches.extend(cr_data[cr])
        
        if matches:
            c = matches[0]
            budget_str = f"AC {c['ac_budget'][0]}-{c['ac_budget'][1]}, HP {c['hp_budget'][0]}-{c['hp_budget'][1]}"
            print(f"CR {target_cr:5.2f} | {c['name'][:25]:25} | AC {c['ac']:2} HP {c['hp']:3} | Budget: {budget_str}")
    
    print()


if __name__ == "__main__":
    analyze_defensive_budgets()
