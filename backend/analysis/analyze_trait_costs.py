#!/usr/bin/env python3
"""
Analyze trait costs in converted creatures to verify budget system is working.
Validates that trait counts match CR budgets and shows distribution.
"""

import json
import statistics
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import KEYWORD_BALANCE, COLOR_TRAIT_BALANCE, get_trait_budget

def extract_trait_names_from_html(traits_html: str) -> list:
    """Extract trait names from HTML by looking at trait-block and property-block elements."""
    traits = []
    if not traits_html:
        return traits
    
    # Look for property-block with <h4> headings (these are trait names)
    # Format: <property-block><h4>Trait Name.</h4>...
    h4_matches = re.findall(r'<h4>([^<]+)\.</h4>', traits_html)
    
    # These are standard D&D abilities, not MTG traits we're budgeting for
    skip_abilities = {
        'Multiattack', 'Bite', 'Claw', 'Slam', 'Charge', 'Breath Weapon',
        'Cone of', 'Ranged Spell Attack', 'Melee Spell Attack', 
        'Keen Hearing and Sight', 'Keen Sight', 'Keen Hearing',
        'Spellcasting', 'Innate Spellcasting', 'Spellcasting (Psion)',
        'Limited Magic Immunity', 'Magic Resistance', 'Legendary Resistance',
        'Regeneration', 'Reactive', 'Telepathy', 'Tremorsense',
        'Relentless', 'Undead Fortitude', 'Brute', 'Ambusher',
        'Swallow', 'Legendary', 'Reaction', 'Legendary Actions',
        'Divine Awareness', 'Awakened Mind', 'Amphibious'
    }
    
    for match in h4_matches:
        trait_name = match.strip()
        # Filter out standard D&D mechanics (not MTG trait costs)
        if trait_name and trait_name not in skip_abilities:
            # Also skip if it contains parenthetical D&D modifiers
            if '(' in trait_name and 'Day' in trait_name:
                # This is "X (N/Day)" format - skip these
                continue
            traits.append(trait_name)
    
    return traits


def get_trait_cost(trait_name: str) -> int:
    """Get cost for a single trait."""
    # Normalize the trait name for comparison
    trait_normalized = trait_name.lower().replace(" ", "")
    
    # Check keyword balance
    for kw in KEYWORD_BALANCE:
        if kw.lower().replace(" ", "") == trait_normalized:
            return KEYWORD_BALANCE[kw].get("cost", 1)
    
    # Check color traits
    for ct in COLOR_TRAIT_BALANCE:
        if ct.lower().replace(" ", "") == trait_normalized:
            return COLOR_TRAIT_BALANCE[ct].get("cost", 1)
    
    # Try direct lookup
    if trait_name in KEYWORD_BALANCE:
        return KEYWORD_BALANCE[trait_name].get("cost", 1)
    if trait_name in COLOR_TRAIT_BALANCE:
        return COLOR_TRAIT_BALANCE[trait_name].get("cost", 1)
    
    return 0  # Unknown trait has no cost


def analyze_trait_distribution():
    """Analyze trait distribution across all creatures."""
    data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
    with open(data_file, "r") as f:
        creatures = json.load(f)
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║          TRAIT COST BUDGET ANALYSIS - D&D CREATURES             ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    cr_trait_counts = {}  # CR -> [trait_counts]
    cr_trait_costs = {}   # CR -> [total_costs]
    violations = []       # Creatures that exceed budget
    
    for creature_name, creature_data in creatures.items():
        if isinstance(creature_data, dict):
            cr_str = creature_data.get("Challenge", "0")
            # Handle fractional CRs and CR format like "4 (1100 XP)"
            try:
                cr_str = cr_str.split()[0]  # Get just the number part
                if "/" in cr_str:
                    cr_num, cr_den = map(int, cr_str.split("/"))
                    cr = cr_num / cr_den
                else:
                    cr = float(cr_str)
            except (ValueError, ZeroDivisionError, AttributeError, IndexError):
                cr = 0
            
            # Extract traits
            traits_html = creature_data.get("Traits", "")
            traits = extract_trait_names_from_html(traits_html)
            
            # Calculate total cost
            total_cost = sum(get_trait_cost(t) for t in traits)
            budget = get_trait_budget(cr)
            
            # Track by CR
            if cr not in cr_trait_counts:
                cr_trait_counts[cr] = []
                cr_trait_costs[cr] = []
            
            cr_trait_counts[cr].append(len(traits))
            cr_trait_costs[cr].append(total_cost)
            
            # Check for violations
            if total_cost > budget:
                violations.append({
                    "name": creature_name,
                    "cr": cr,
                    "traits": traits,
                    "cost": total_cost,
                    "budget": budget
                })
    
    # Print summary by CR
    print("CR Range      | Avg Traits | Avg Cost | Budget | Creatures | Violations")
    print("─" * 79)
    
    sorted_crs = sorted(cr_trait_counts.keys())
    for cr in sorted_crs:
        counts = cr_trait_counts[cr]
        costs = cr_trait_costs[cr]
        budget = get_trait_budget(cr)
        avg_count = statistics.mean(counts) if counts else 0
        avg_cost = statistics.mean(costs) if costs else 0
        num_creatures = len(counts)
        
        # Count violations for this CR
        cr_violations = sum(1 for v in violations if v["cr"] == cr)
        
        cr_display = f"{cr:.1f}" if cr % 1 != 0 else f"{int(cr)}"
        print(f"CR {cr_display:5} | {avg_count:10.2f} | {avg_cost:8.2f} | {budget:6} | {num_creatures:9} | {cr_violations:10}")
    
    print()
    print("TRAIT DISTRIBUTION STATISTICS")
    print("─" * 79)
    all_counts = [c for counts in cr_trait_counts.values() for c in counts]
    all_costs = [c for costs in cr_trait_costs.values() for c in costs]
    
    print(f"Total creatures analyzed: {len(creatures)}")
    print(f"Creatures with traits: {sum(1 for c in all_counts if c > 0)}")
    print(f"Average traits per creature: {statistics.mean(all_counts):.2f}")
    print(f"Median traits per creature: {statistics.median(all_counts):.1f}")
    print(f"Average trait cost per creature: {statistics.mean(all_costs):.2f}")
    print(f"Max traits found: {max(all_counts) if all_counts else 0}")
    print(f"Max cost found: {max(all_costs) if all_costs else 0}")
    print()
    
    # Print violations if any
    if violations:
        print(f"⚠️  BUDGET VIOLATIONS: {len(violations)} creatures exceed their CR budget!")
        print("─" * 79)
        for v in violations[:10]:  # Show first 10
            traits_str = ", ".join(v["traits"][:3])
            if len(v["traits"]) > 3:
                traits_str += f", +{len(v['traits']) - 3} more"
            print(f"  {v['name']:30} CR {v['cr']:5.1f} | Cost {v['cost']:2}/{v['budget']:2} | {traits_str}")
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more violations")
    else:
        print("✓ All creatures respect their trait budgets!")
    
    print()
    
    # Show sample creatures to verify correct behavior
    print("SAMPLE CREATURES BY CR")
    print("─" * 79)
    
    sample_crs = [0.2, 1, 3, 5, 9, 15, 20, 30]
    for target_cr in sample_crs:
        # Find a creature near this CR
        sample = None
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
                
                if abs(cr - target_cr) < 0.6:  # Within 0.5 CR
                    traits_html = creature_data.get("Traits", "")
                    traits = extract_trait_names_from_html(traits_html)
                    total_cost = sum(get_trait_cost(t) for t in traits)
                    budget = get_trait_budget(cr)
                    
                    sample = {
                        "name": creature_name,
                        "cr": cr,
                        "traits": traits[:4],  # First 4 traits
                        "cost": total_cost,
                        "budget": budget
                    }
                    break
        
        if sample:
            traits_str = ", ".join(sample["traits"]) if sample["traits"] else "(none)"
            print(f"  {sample['name']:30} CR {sample['cr']:5.1f} | {traits_str[:40]:40} | Cost {sample['cost']}/{sample['budget']}")


if __name__ == "__main__":
    analyze_trait_distribution()
