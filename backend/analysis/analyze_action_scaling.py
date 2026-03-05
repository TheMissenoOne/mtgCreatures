#!/usr/bin/env python3
"""
Analyze CR-based action scaling to verify damage and bonuses match CR tier.
Shows before/after comparisons of attack bonuses and damage dice.
"""

import json
import re
from collections import defaultdict
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def extract_attack_bonus(action_html: str) -> list:
    """Extract all attack bonuses from action HTML."""
    pattern = r'\+(\d+) to hit'
    matches = re.findall(pattern, action_html)
    return [int(m) for m in matches]


def extract_damage_expressions(action_html: str) -> list:
    """Extract all damage expressions from action HTML."""
    pattern = r'(\d+d\d+(?:\+\d+)?)'
    matches = re.findall(pattern, action_html)
    return matches


def parse_damage_expr(expr: str) -> tuple:
    """Parse damage expression into (dice_count, die_size, bonus)."""
    match = re.match(r'(\d+)d(\d+)(?:\+(\d+))?', expr)
    if match:
        bonus = int(match.group(3)) if match.group(3) else 0
        return (int(match.group(1)), int(match.group(2)), bonus)
    return None


def get_avg_damage(dice_count: int, die_size: int, bonus: int) -> float:
    """Calculate average damage from dice expression."""
    avg_die = (die_size + 1) / 2.0
    return dice_count * avg_die + bonus


def analyze_action_scaling():
    """Analyze action damage and bonuses by CR tier."""
    data_file = Path(__file__).parent.parent.parent / "data" / "output" / "final.json"
    with open(data_file, "r") as f:
        creatures = json.load(f)
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     CR-BASED ACTION DAMAGE & ATTACK BONUS SCALING ANALYSIS      ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    cr_data = defaultdict(list)  # CR -> list of (attack_bonuses, damages)
    
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
            
            # Extract actions
            actions_html = creature_data.get("Actions", "") or ""
            
            attack_bonuses = extract_attack_bonus(actions_html)
            damage_exprs = extract_damage_expressions(actions_html)
            
            if attack_bonuses or damage_exprs:
                cr_data[cr].append({
                    "name": creature_name,
                    "bonuses": attack_bonuses,
                    "damages": damage_exprs
                })
    
    # Print analysis by CR
    print("CR Tier  | Avg Attack Bonus | Attack Bonus Range | Avg Damage | Max Avg Dmg | Avg Damage Expr")
    print("─" * 105)
    
    for cr in sorted(cr_data.keys()):
        creatures_list = cr_data[cr]
        if not creatures_list:
            continue
        
        all_bonuses = []
        all_damages = []
        
        for creature in creatures_list:
            all_bonuses.extend(creature["bonuses"])
            all_damages.extend(creature["damages"])
        
        # Calculate statistics
        avg_bonus = sum(all_bonuses) / len(all_bonuses) if all_bonuses else 0
        min_bonus = min(all_bonuses) if all_bonuses else 0
        max_bonus = max(all_bonuses) if all_bonuses else 0
        
        # Calculate damage statistics
        damage_values = []
        for dmg_expr in all_damages:
            parsed = parse_damage_expr(dmg_expr)
            if parsed:
                damage_values.append(get_avg_damage(*parsed))
        
        avg_damage = sum(damage_values) / len(damage_values) if damage_values else 0
        max_damage = max(damage_values) if damage_values else 0
        
        # Common damage expression
        if all_damages:
            most_common_dmg = max(set(all_damages), key=all_damages.count)
        else:
            most_common_dmg = "N/A"
        
        cr_display = f"{cr:.1f}" if cr % 1 != 0 else f"{int(cr)}"
        print(f"CR {cr_display:4} | {avg_bonus:15.1f} | {min_bonus:3}-{max_bonus:3} (range) | {avg_damage:10.2f} | {max_damage:11.2f} | {most_common_dmg}")
    
    print()
    print("SCALING SUMMARY BY CR TIER")
    print("─" * 105)
    
    tier_ranges = [
        (0, 3, "Low"),
        (4, 5, "Mid-Low"),
        (6, 8, "Mid"),
        (9, 12, "High"),
        (13, 20, "Very High"),
        (20, 30, "Legendary")
    ]
    
    for min_cr, max_cr, tier_name in tier_ranges:
        bonuses_in_tier = []
        damages_in_tier = []
        
        for cr in cr_data:
            if min_cr <= cr <= max_cr:
                for creature in cr_data[cr]:
                    bonuses_in_tier.extend(creature["bonuses"])
                    damages_in_tier.extend(creature["damages"])
        
        if bonuses_in_tier or damages_in_tier:
            avg_bonus = sum(bonuses_in_tier) / len(bonuses_in_tier) if bonuses_in_tier else 0
            
            damage_values = []
            for dmg_expr in damages_in_tier:
                parsed = parse_damage_expr(dmg_expr)
                if parsed:
                    damage_values.append(get_avg_damage(*parsed))
            
            avg_damage = sum(damage_values) / len(damage_values) if damage_values else 0
            max_damage = max(damage_values) if damage_values else 0
            
            count = len([c for cr in cr_data if min_cr <= cr <= max_cr for c in cr_data[cr]])
            print(f"{tier_name:12} (CR {min_cr:2}-{max_cr:2}) | {count:3} creatures | Avg Bonus: {avg_bonus:5.1f} | Avg Dmg: {avg_damage:6.2f} | Max: {max_damage:6.2f}")
    
    print()
    print("SAMPLE CREATURES WITH SCALED ACTIONS")
    print("─" * 105)
    
    sample_crs = [1, 3, 5, 8, 10, 15, 20]
    for target_cr in sample_crs:
        # Find creatures near target CR
        samples = []
        for cr in cr_data:
            if abs(cr - target_cr) < 1.5:
                for creature in cr_data[cr][:1]:  # Just first one per CR
                    samples.append((cr, creature))
        
        if samples:
            cr, creature = samples[0]
            bonuses_str = ", ".join(map(str, creature["bonuses"][:3])) if creature["bonuses"] else "N/A"
            damages_str = ", ".join(creature["damages"][:3]) if creature["damages"] else "N/A"
            
            cr_display = f"{cr:.1f}" if cr % 1 != 0 else f"{int(cr)}"
            print(f"CR {cr_display:4} | {creature['name']:25} | Bonuses: {bonuses_str:15} | Damages: {damages_str}")
    
    print()


if __name__ == "__main__":
    analyze_action_scaling()
