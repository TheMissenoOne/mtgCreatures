"""D&D statistics calculation utilities."""

import math
from fractions import Fraction
from typing import Dict, Any

from config import ATTRIBUTES, CHALLENGE_RATINGS


def parse_armor_class(ac_value: Any) -> int:
    """Parse armor class, handling string format."""
    if isinstance(ac_value, str):
        return int(ac_value.split()[0])
    return int(ac_value)


def parse_hit_points(hp_value: Any) -> int:
    """Parse hit points, handling string format."""
    if isinstance(hp_value, str):
        return int(hp_value.split()[0])
    return int(hp_value)


def calculate_ability_modifier(ability_score: int) -> int:
    """Calculate D&D ability modifier from ability score."""
    return (ability_score - 10) // 2


def get_cr_from_challenge(challenge_str: str) -> str:
    """Extract CR value from challenge string like '3 (700 XP)'."""
    return challenge_str.split()[0]


def calculate_base_creature_stats(cr: str) -> Dict[str, int]:
    """
    Get baseline stats for a given challenge rating.
    
    Args:
        cr: Challenge rating as string (e.g., "3", "1/2")
        
    Returns:
        Dictionary with base AC and HP for the CR
    """
    if cr not in CHALLENGE_RATINGS:
        return {"Armor Class": 10, "Hit Points": 10}
    return {
        "Armor Class": CHALLENGE_RATINGS[cr]["Armor Class"],
        "Hit Points": CHALLENGE_RATINGS[cr]["Hit Points"],
    }


class StatBlockCalculator:
    """Calculates D&D stat block values for creatures."""

    @staticmethod
    def calculate_creature_stats_from_baseline(
        creature_base_cr: str, creature_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate adjusted stats for a creature based on baseline stats.
        
        Args:
            creature_base_cr: Creature's baseline CR
            creature_data: Creature data dictionary
            
        Returns:
            Updated creature data with calculated stats
        """
        updated = creature_data.copy()
        
        if creature_base_cr not in CHALLENGE_RATINGS:
            return updated

        baseline_cr_stats = CHALLENGE_RATINGS[creature_base_cr]
        
        # Parse and adjust AC and HP
        actual_ac = parse_armor_class(updated["Armor Class"])
        actual_hp = parse_hit_points(updated["Hit Points"])
        
        # Calculate modifiers for each ability
        for attr in ATTRIBUTES:
            attr_score = int(float(updated.get(attr, 10)))
            baseline_score = 10 + Fraction(creature_base_cr) * Fraction(3, 4)
            modifier = int(attr_score - baseline_score)
            
            updated[f"{attr}_mod"] = modifier
            updated[attr] = 10 + modifier

        # Adjust AC and HP based on baseline
        updated["Armor Class"] = baseline_cr_stats["Armor Class"] - actual_ac
        updated["Hit Points"] = actual_hp

        return updated

    @staticmethod
    def merge_stats_from_types(
        base_creature: Dict[str, Any],
        type_creatures: list[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Merge stats from multiple creature types.
        
        Args:
            base_creature: Base creature stats
            type_creatures: List of creature type stats to merge
            
        Returns:
            Updated creature with merged stats
        """
        result = base_creature.copy()
        
        if not type_creatures:
            return result

        # Average ability scores across types
        for attr in ATTRIBUTES:
            scores = [int(base_creature.get(attr, 10))]
            scores.extend(int(t.get(attr, 10)) for t in type_creatures)
            
            avg_score = sum(scores) // len(scores)
            result[attr] = avg_score
            result[f"{attr}_mod"] = calculate_ability_modifier(avg_score)

        # Average HP and AC
        hp_values = [int(base_creature.get("Hit Points", 10))]
        hp_values.extend(int(t.get("Hit Points", 10)) for t in type_creatures)
        result["Hit Points"] = sum(hp_values) // len(hp_values)

        ac_values = [int(base_creature.get("Armor Class", 10))]
        ac_values.extend(int(t.get("Armor Class", 10)) for t in type_creatures)
        result["Armor Class"] = sum(ac_values) // len(ac_values)

        return result

    @staticmethod
    def calculate_ravnica_card_cr(
        rarity_multiplier: float, cmc: float, power_toughness: float
    ) -> int:
        """
        Calculate Challenge Rating for a Ravnica card.
        
        Args:
            rarity_multiplier: Card rarity value
            cmc: Converted mana cost
            power_toughness: Sum of power and toughness
            
        Returns:
            Calculated CR as integer
        """
        if power_toughness <= 0 or cmc <= 0:
            return 0

        try:
            cr = math.log(rarity_multiplier / (cmc / power_toughness)) + cmc
            return max(0, int(round(cr)))
        except (ValueError, ZeroDivisionError):
            return 0

def apply_trait_adjustments(
    creature: Dict[str, Any],
    cr: int,
    keywords: List[str],
    color_traits: List[str],
) -> Dict[str, Any]:
    """
    Apply keyword and color trait adjustments to creature stats and CR.
    
    Args:
        creature: Base creature data
        cr: Base challenge rating
        keywords: List of MTG keywords to apply
        color_traits: List of color/guild traits to apply
        
    Returns:
        Updated creature creature with adjustments applied
    """
    from config import KEYWORD_BALANCE, COLOR_TRAIT_BALANCE, CHALLENGE_RATINGS
    
    result = creature.copy()
    
    cr_offense = 0.0
    cr_defense = 0.0
    dpr_bonus = 0.0
    hp_delta = 0
    hp_multiplier = 1.0
    save_dc_delta = 0
    
    # Apply keyword adjustments
    for keyword in keywords:
        if keyword in KEYWORD_BALANCE:
            balance = KEYWORD_BALANCE[keyword]
            cr_offense += balance.get("cr_offense", 0.0)
            cr_defense += balance.get("cr_defense", 0.0)
            dpr_bonus += balance.get("dpr_bonus", 0.0)
            hp_delta += balance.get("hp_delta", 0)
            save_dc_delta += balance.get("save_dc_delta", 0)
            if "hp_multiplier" in balance:
                hp_multiplier *= balance["hp_multiplier"]
    
    # Apply color trait adjustments
    for trait in color_traits:
        if trait in COLOR_TRAIT_BALANCE:
            balance = COLOR_TRAIT_BALANCE[trait]
            cr_offense += balance.get("cr_offense", 0.0)
            cr_defense += balance.get("cr_defense", 0.0)
            dpr_bonus += balance.get("dpr_bonus", 0.0)
            hp_delta += balance.get("hp_delta", 0)
            save_dc_delta += balance.get("save_dc_delta", 0)
            if "hp_multiplier" in balance:
                hp_multiplier *= balance["hp_multiplier"]
    
    # Calculate adjusted CR
    cr_combined = (cr_offense + cr_defense) / 2.0
    adjusted_cr = cr + cr_combined
    
    # Clamp to valid CR range
    cr_keys = list(CHALLENGE_RATINGS.keys())
    try:
        cr_int = max(0, min(30, int(round(adjusted_cr))))
        cr_str = str(cr_int)
        if cr_str in CHALLENGE_RATINGS:
            result.update(CHALLENGE_RATINGS[cr_str])
    except (ValueError, IndexError):
        pass  # Keep original CR
    
    # Apply HP adjustments
    if "Hit Points" in result:
        base_hp = int(result["Hit Points"])
        result["Hit Points"] = int(base_hp * hp_multiplier + hp_delta)
    
    # Apply Save DC adjustment (if saving throw fields exist)
    if save_dc_delta > 0:
        result["_save_dc_bonus"] = save_dc_delta
    
    # Store DPR bonus for informational purposes
    if dpr_bonus > 0:
        result["_dpr_bonus"] = dpr_bonus
    
    return result

