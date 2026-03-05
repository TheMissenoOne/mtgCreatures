"""D&D statistics calculation utilities."""

import math
from fractions import Fraction
from typing import Dict, Any

from config import ATTRIBUTES, CHALLENGE_RATINGS


# AC and HP budgets per CR to prevent power creep
AC_BUDGETS = {
    # CR: (min_ac, max_ac) - reasonable AC range for creatures
    0: (10, 11), 1: (10, 12), 2: (10, 13), 3: (11, 14),
    4: (12, 14), 5: (12, 15), 6: (13, 15), 7: (13, 16),
    8: (14, 16), 9: (14, 17), 10: (15, 17), 11: (15, 18),
    12: (15, 18), 13: (16, 18), 14: (16, 19), 15: (16, 19),
    16: (17, 19), 17: (17, 20), 18: (17, 20), 19: (18, 20),
    20: (18, 21), 21: (19, 21), 22: (19, 21), 23: (20, 21),
    24: (20, 22), 25: (20, 22), 26: (21, 22), 27: (21, 22),
    28: (21, 22), 29: (21, 22), 30: (21, 22),
}

HP_BUDGETS = {
    # CR: (min_hp, max_hp) - reasonable HP range for creatures
    0: (1, 6), 0.125: (1, 3), 0.25: (1, 6), 0.5: (1, 6),
    1: (6, 20), 2: (20, 35), 3: (26, 40), 4: (35, 50),
    5: (40, 65), 6: (45, 75), 7: (50, 85), 8: (65, 100),
    9: (75, 110), 10: (85, 130), 11: (100, 145), 12: (110, 160),
    13: (130, 190), 14: (150, 210), 15: (160, 240), 16: (190, 270),
    17: (210, 300), 18: (240, 330), 19: (270, 360), 20: (300, 400),
    21: (330, 430), 22: (360, 460), 23: (400, 500), 24: (430, 540),
    25: (460, 580), 26: (500, 620), 27: (540, 660), 28: (580, 700),
    29: (620, 740), 30: (660, 780),
}


def get_ac_budget(cr: float) -> tuple:
    """Return (min_ac, max_ac) tuple for given CR."""
    cr_int = int(cr)
    if cr_int in AC_BUDGETS:
        return AC_BUDGETS[cr_int]
    # For fractional CR like 1/8, 1/4, 1/2
    if cr == 0.125:
        return AC_BUDGETS[0.125]
    if cr == 0.25:
        return AC_BUDGETS[0.25]
    if cr == 0.5:
        return AC_BUDGETS[0.5]
    # Fallback to tier-by-tier
    if cr < 1:
        return AC_BUDGETS[0]
    return AC_BUDGETS.get(min(30, cr_int), AC_BUDGETS[30])


def get_hp_budget(cr: float) -> tuple:
    """Return (min_hp, max_hp) tuple for given CR."""
    cr_int = int(cr)
    if cr_int in HP_BUDGETS:
        return HP_BUDGETS[cr_int]
    # For fractional CR
    if cr == 0.125:
        return HP_BUDGETS[0.125]
    if cr == 0.25:
        return HP_BUDGETS[0.25]
    if cr == 0.5:
        return HP_BUDGETS[0.5]
    # Fallback
    if cr < 1:
        return HP_BUDGETS[0]
    return HP_BUDGETS.get(min(30, cr_int), HP_BUDGETS[30])


def validate_ac(ac: int, cr: float) -> int:
    """
    Validate and potentially cap AC to be appropriate for CR.
    Prevents low-CR creatures from having extremely high AC.
    
    Args:
        ac: Proposed armor class
        cr: Challenge rating
        
    Returns:
        Validated AC value (may be capped)
    """
    min_ac, max_ac = get_ac_budget(cr)
    
    if ac < min_ac:
        # AC too low - not typical for this CR
        return min_ac
    elif ac > max_ac:
        # AC too high - cap it
        return max_ac
    return ac


def validate_hp(hp: int, cr: float) -> int:
    """
    Validate and potentially cap HP to be appropriate for CR.
    Prevents low-CR creatures from having excessive hit points.
    
    Args:
        hp: Proposed hit points
        cr: Challenge rating
        
    Returns:
        Validated HP value (may be capped)
    """
    min_hp, max_hp = get_hp_budget(cr)
    
    if hp < min_hp:
        # HP too low for this CR - bring up to minimum
        return min_hp
    elif hp > max_hp:
        # HP too high for this CR - cap it
        return max_hp
    return hp


def apply_defensive_budgets(creature: Dict[str, Any], cr: float) -> Dict[str, Any]:
    """
    Validate and cap AC and HP to be appropriate for CR level.
    Prevents low-CR creatures from being overpowered defensively.
    
    Args:
        creature: Creature data
        cr: Challenge rating (float)
        
    Returns:
        Updated creature with validated AC and HP
    """
    result = creature.copy()
    
    # Validate and potentially cap AC
    if "Armor Class" in result:
        try:
            ac = parse_armor_class(result["Armor Class"])
            validated_ac = validate_ac(ac, cr)
            if validated_ac != ac:
                result["Armor Class"] = str(validated_ac)
        except (ValueError, TypeError):
            pass  # Keep original if parsing fails
    
    # Validate and potentially cap HP
    if "Hit Points" in result:
        try:
            hp = parse_hit_points(result["Hit Points"])
            validated_hp = validate_hp(hp, cr)
            if validated_hp != hp:
                result["Hit Points"] = str(validated_hp)
        except (ValueError, TypeError):
            pass  # Keep original if parsing fails
    
    return result

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


def scale_damage_expression(damage_expr: str, cr: float) -> str:
    """
    Scale a damage expression (e.g., '2d6+3') based on CR.
    
    Scaling strategy:
    - CR 0-3: No scaling (base game damage is appropriate)
    - CR 4-5: +1 damage bonus
    - CR 6-8: +2 damage bonus or upgrade one die
    - CR 9-12: +3 damage bonus or upgrade dice (d6→d8, d8→d10)
    - CR 13+: +4+ damage bonus or multiple die upgrades
    
    Args:
        damage_expr: String like "2d6+3" or "1d10" or "3d8"
        cr: Challenge rating (float)
        
    Returns:
        Scaled damage expression
    """
    import re
    
    # Pattern: XdY+Z where X=dice count, Y=die size, Z=bonus (optional)
    match = re.match(r'(\d+)d(\d+)(?:\+(\d+))?', damage_expr.strip())
    if not match:
        return damage_expr  # Return unchanged if can't parse
    
    dice_count = int(match.group(1))
    die_size = int(match.group(2))
    bonus = int(match.group(3)) if match.group(3) else 0
    
    # Determine scaling tier
    if cr <= 3:
        # No scaling for low CR
        return damage_expr
    elif cr <= 5:
        # Small bonus for mid-low CR
        bonus += 1
    elif cr <= 8:
        # Medium scaling: bonus or upgrade die
        if die_size < 12:
            die_upgrade = {4: 6, 6: 8, 8: 10, 10: 12}
            die_size = die_upgrade.get(die_size, die_size)
        bonus += 2
    elif cr <= 12:
        # High scaling: upgrade die + bonus
        if die_size < 12:
            die_upgrade = {4: 8, 6: 10, 8: 12, 10: 12}
            die_size = die_upgrade.get(die_size, die_size)
        bonus += 3
    else:
        # Very high CR: potentially add dice + upgrade + bonus
        if dice_count < 5 and die_size >= 8:
            dice_count += 1
        if die_size < 12:
            die_upgrade = {4: 10, 6: 12, 8: 12, 10: 12}
            die_size = die_upgrade.get(die_size, die_size)
        bonus += 4
    
    # Rebuild expression
    result = f"{dice_count}d{die_size}"
    if bonus > 0:
        result += f"+{bonus}"
    
    return result


def scale_attack_bonus(bonus: int, cr: float) -> int:
    """
    Scale attack bonus based on CR.
    
    Args:
        bonus: Base attack bonus
        cr: Challenge rating
        
    Returns:
        Scaled attack bonus
    """
    if cr <= 3:
        return bonus
    elif cr <= 5:
        return bonus + 1
    elif cr <= 8:
        return bonus + 2
    elif cr <= 12:
        return bonus + 3
    elif cr <= 20:
        return bonus + 4
    else:
        return bonus + 5


def scale_action_damage(action_html: str, cr: float) -> str:
    """
    Scale all damage expressions and attack bonuses in an action block.
    
    Args:
        action_html: HTML string containing action description
        cr: Challenge rating
        
    Returns:
        Updated HTML with scaled damage/bonuses
    """
    import re
    
    result = action_html
    
    # Scale damage expressions (pattern: XdY+Z)
    damage_pattern = r'(\d+d\d+(?:\+\d+)?)'
    damage_matches = re.finditer(damage_pattern, result)
    
    replacements = []
    for match in damage_matches:
        original = match.group(1)
        scaled = scale_damage_expression(original, cr)
        if scaled != original:
            replacements.append((original, scaled))
    
    # Apply replacements (avoid duplicate replacements)
    seen = set()
    for original, scaled in replacements:
        if original not in seen:
            result = result.replace(original, scaled, 1)
            seen.add(original)
    
    # Scale attack bonuses (pattern: +N to hit)
    attack_bonus_pattern = r'\+(\d+) to hit'
    attack_matches = list(re.finditer(attack_bonus_pattern, result))
    
    # Process in reverse to maintain string positions
    for match in reversed(attack_matches):
        original_bonus = int(match.group(1))
        scaled_bonus = scale_attack_bonus(original_bonus, cr)
        
        if scaled_bonus != original_bonus:
            start, end = match.span(1)
            result = result[:start] + str(scaled_bonus) + result[end:]
    
    return result


def apply_action_scaling(creature: Dict[str, Any], cr: float) -> Dict[str, Any]:
    """
    Apply CR-based scaling to all creature actions and effects.
    
    Args:
        creature: Creature data
        cr: Challenge rating
        
    Returns:
        Updated creature with scaled actions
    """
    result = creature.copy()
    
    # Scale Actions field
    if "Actions" in result and result["Actions"]:
        result["Actions"] = scale_action_damage(result["Actions"], cr)
    
    # Scale Legendary Actions field (if present)
    if "Legendary Actions" in result and result["Legendary Actions"]:
        result["Legendary Actions"] = scale_action_damage(result["Legendary Actions"], cr)
    
    # Scale Reactions field (if present)
    if "Reactions" in result and result["Reactions"]:
        result["Reactions"] = scale_action_damage(result["Reactions"], cr)
    
    return result

def apply_trait_adjustments(
    creature: Dict[str, Any],
    cr: float,
    keywords: List[str],
    color_traits: List[str],
) -> Dict[str, Any]:
    """
    Apply keyword and color trait adjustments to creature stats and CR.
    Respects trait cost budgets to prevent overpowered low-CR creatures.
    
    Args:
        creature: Base creature data
        cr: Base challenge rating (float, e.g., 2.5, 3.0)
        keywords: List of MTG keywords to apply
        color_traits: List of color/guild traits to apply
        
    Returns:
        Updated creature with adjustments applied (respects trait budget)
    """
    from config import KEYWORD_BALANCE, COLOR_TRAIT_BALANCE, CHALLENGE_RATINGS, get_trait_budget
    
    result = creature.copy()
    
    # Get trait budget for this CR
    trait_budget = get_trait_budget(cr)
    trait_cost_spent = 0
    applied_keywords = []
    applied_color_traits = []
    
    cr_offense = 0.0
    cr_defense = 0.0
    dpr_bonus = 0.0
    hp_delta = 0
    hp_multiplier = 1.0
    save_dc_delta = 0
    
    # Apply keyword adjustments (prioritize by cost: cheapest first)
    keyword_data = [
        (kw, KEYWORD_BALANCE.get(kw, {}))
        for kw in keywords
        if kw in KEYWORD_BALANCE
    ]
    # Sort by cost (ascending): apply cheaper traits first within budget
    keyword_data.sort(key=lambda x: x[1].get("cost", 999))
    
    for keyword, balance in keyword_data:
        trait_cost = balance.get("cost", 1)
        
        # Check if adding this trait exceeds budget
        if trait_cost_spent + trait_cost <= trait_budget:
            trait_cost_spent += trait_cost
            applied_keywords.append(keyword)
            
            cr_offense += balance.get("cr_offense", 0.0)
            cr_defense += balance.get("cr_defense", 0.0)
            dpr_bonus += balance.get("dpr_bonus", 0.0)
            hp_delta += balance.get("hp_delta", 0)
            save_dc_delta += balance.get("save_dc_delta", 0)
            # hp_multiplier is multiplicative (only first multiplier usually)
            if balance.get("hp_multiplier", 1.0) != 1.0:
                hp_multiplier *= balance.get("hp_multiplier", 1.0)
    
    # Apply color trait adjustments (also respects budget)
    color_trait_data = [
        (ct, COLOR_TRAIT_BALANCE.get(ct, {}))
        for ct in color_traits
        if ct in COLOR_TRAIT_BALANCE
    ]
    # Sort by cost (ascending): apply cheaper traits first within budget
    color_trait_data.sort(key=lambda x: x[1].get("cost", 999))
    
    for color_trait, balance in color_trait_data:
        trait_cost = balance.get("cost", 1)
        
        # Check if adding this trait exceeds budget
        if trait_cost_spent + trait_cost <= trait_budget:
            trait_cost_spent += trait_cost
            applied_color_traits.append(color_trait)
            
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
    
    # Store applied traits for creature converter to use in HTML generation
    result["_applied_keywords"] = applied_keywords
    result["_applied_color_traits"] = applied_color_traits
    
    return result

