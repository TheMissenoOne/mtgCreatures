"""Creature processing and conversion logic."""

import logging
import re
from typing import Dict, Any, List
from fractions import Fraction

from config import (
    ATTRIBUTES,
    CHALLENGE_RATINGS,
    KEYWORDS,
    COLOR_TRAITS,
    RARITY_MULTIPLIERS,
)
from stats_calculator import (
    StatBlockCalculator,
    apply_trait_adjustments,
    parse_armor_class,
    parse_hit_points,
    get_cr_from_challenge,
)
from file_utils import append_to_file

logger = logging.getLogger(__name__)


class MonsterProcessor:
    """Processes base monster data from D&D sources."""

    def __init__(self, new_types_file: str = "newTypes.txt"):
        self.new_types_file = new_types_file

    def process_monsters(
        self, creatures: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Process monster list and calculate modifiers.
        
        Args:
            creatures: List of creature data
            
        Returns:
            Dictionary of processed creatures by name
        """
        processed = {}
        
        for creature in creatures:
            try:
                cr = get_cr_from_challenge(creature.get("Challenge", "0"))
                
                if cr not in CHALLENGE_RATINGS:
                    logger.warning(
                        f"Unknown CR {cr} for creature {creature.get('name')}"
                    )
                    continue

                # Calculate stats
                creature_copy = creature.copy()
                creature_copy["Armor Class"] = parse_armor_class(
                    creature_copy["Armor Class"]
                )
                creature_copy["Hit Points"] = parse_hit_points(
                    creature_copy["Hit Points"]
                )

                # Calculate ability modifiers
                for attr in ATTRIBUTES:
                    base_score = int(float(creature_copy.get(attr, 10)))
                    expected_base = 10 + Fraction(cr) * Fraction(3, 4)
                    modifier = int(base_score - expected_base)
                    
                    creature_copy[f"{attr}_mod"] = modifier
                    creature_copy[attr] = 10 + modifier

                # Adjust AC and HP to baseline
                baseline = CHALLENGE_RATINGS[cr]
                creature_copy["Armor Class"] = (
                    baseline["Armor Class"] - creature_copy["Armor Class"]
                )
                creature_copy["Hit Points"] = int(creature_copy["Hit Points"])

                processed[creature_copy["name"]] = creature_copy

            except Exception as e:
                logger.error(
                    f"Error processing creature {creature.get('name')}: {e}"
                )
                continue

        logger.info(f"Processed {len(processed)} monsters")
        return processed


class RavnicaCardConverter:
    """Converts Magic: The Gathering Ravnica cards to D&D creatures."""

    def __init__(self, base_creatures: Dict[str, Any]):
        self.base_creatures = base_creatures
        self.new_types = set()

    def convert_cards(self, cards: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Convert MTG cards to D&D creatures.
        
        Args:
            cards: List of MTG card data
            
        Returns:
            Dictionary of converted creatures by name
        """
        converted = {}
        
        # Filter valid cards (numeric power and toughness)
        valid_cards = [
            card
            for card in cards
            if (
                card.get("toughness", "").isnumeric()
                and card.get("power", "").isnumeric()
                and (float(card.get("power", 0)) + float(card.get("toughness", 0)))
                > 0
            )
        ]

        logger.info(f"Converting {len(valid_cards)} valid cards")
        
        for i, card in enumerate(valid_cards):
            if (i + 1) % max(1, len(valid_cards) // 10) == 0:
                logger.debug(f"Processed {i + 1}/{len(valid_cards)} cards")
            
            try:
                creature = self._convert_single_card(card)
                if creature:
                    converted[creature["name"]] = creature
            except Exception as e:
                logger.error(f"Error converting card {card.get('name')}: {e}")
                continue

        logger.info(f"Converted {len(converted)} creatures")
        return converted

    def _convert_single_card(self, card: Dict[str, Any]) -> Dict[str, Any] | None:
        """Convert a single MTG card to D&D creature."""
        creature = card.copy()
        
        # Initialize D&D fields
        creature.update(
            {
                "Actions": "",
                "Languages": "",
                "Skills": "",
                "Senses": "",
                "Speed": "",
                "meta": "",
                "Damage Immunities": "",
                "Condition Immunities": "",
                "Damage Resistances": "",
            }
        )

        # Extract creature types
        types = self._extract_creature_types(card)
        
        # Calculate CR
        creature_cr = self._calculate_creature_cr(card, types)
        
        # Apply challenge rating data
        if str(creature_cr) in CHALLENGE_RATINGS:
            creature.update(CHALLENGE_RATINGS[str(creature_cr)])
        
        # Calculate ability scores
        self._calculate_abilities(creature, creature_cr, types)
        
        # Merge type-based attributes
        self._merge_type_attributes(creature, types)
        
        # Convert flavor text
        if "flavor_text" in card:
            creature["description"] = card["flavor_text"]

        # Extract and apply traits
        keywords = self._extract_keywords_from_card(card)
        color_traits = self._extract_color_traits(card)
        
        # Apply trait adjustments to stats (with budget filtering built-in)
        # This will return filtered lists of applied traits
        adjusted_creature = apply_trait_adjustments(
            creature, creature_cr, keywords, color_traits
        )
        creature.update(adjusted_creature)
        
        # IMPORTANT: Use only the accepted traits (those within budget) for HTML
        applied_keywords = adjusted_creature.get("_applied_keywords", [])
        applied_color_traits = adjusted_creature.get("_applied_color_traits", [])
        
        # Apply keyword traits to Traits field (only budget-approved traits)
        self._apply_keyword_traits(creature, applied_keywords)
        
        # Apply color traits (only budget-approved traits)
        self._apply_color_traits_from_list(creature, applied_color_traits)
        
        # Apply CR-based action scaling (damage and attack bonuses)
        from stats_calculator import apply_action_scaling, apply_defensive_budgets
        scaled_creature = apply_action_scaling(creature, creature_cr)
        creature.update(scaled_creature)
        
        # Apply CR-based defensive budgeting (cap AC and HP to CR-appropriate levels)
        defensive_creature = apply_defensive_budgets(creature, creature_cr)
        creature.update(defensive_creature)
        
        # Clean up internal tracking fields
        creature.pop("_applied_keywords", None)
        creature.pop("_applied_color_traits", None)
        
        return creature

    def _extract_creature_types(self, card: Dict[str, Any]) -> List[str]:
        """Extract and validate creature types from card name and type line."""
        types = []
        
        # Check card name for type matches
        for name_part in card.get("name", "").split():
            if name_part in self.base_creatures:
                types.append(name_part)
            else:
                self.new_types.add(name_part)

        # Extract from type line
        if "type_line" in card and " — " in card["type_line"]:
            main_type = card["type_line"].split(" — ")[1].split()
            types.extend(main_type)

        return list(set(types))  # Remove duplicates

    def _calculate_creature_cr(
        self, card: Dict[str, Any], types: List[str]
    ) -> int:
        """Calculate base CR for card, adjusted by creature types."""
        rarity = card.get("rarity", "common")
        cmc = float(card.get("cmc", 1))
        power = float(card.get("power", 0))
        toughness = float(card.get("toughness", 0))
        
        multiplier = RARITY_MULTIPLIERS.get(rarity, 1)
        
        base_cr = StatBlockCalculator.calculate_ravnica_card_cr(multiplier, cmc, power + toughness)

        # Adjust by type CRs
        for creature_type in types:
            if creature_type in self.base_creatures:
                type_cr_str = get_cr_from_challenge(
                    self.base_creatures[creature_type].get("Challenge", "0")
                )
                try:
                    type_cr = int(Fraction(type_cr_str))
                    if type_cr > base_cr:
                        base_cr = int(round(base_cr + Fraction(type_cr, 5)))
                except (ValueError, ZeroDivisionError):
                    pass

        return max(0, base_cr)

    def _calculate_abilities(
        self, creature: Dict[str, Any], cr: int, types: List[str]
    ) -> None:
        """Calculate ability scores for creature."""
        cr_str = str(cr)
        
        # Start with CR baseline
        for attr in ATTRIBUTES:
            creature[attr] = round(10 + Fraction(cr_str) * Fraction(3, 4))

        # Merge type abilities
        type_creatures = [
            self.base_creatures[t] for t in types if t in self.base_creatures
        ]
        
        if type_creatures:
            merged = StatBlockCalculator.merge_stats_from_types(creature, type_creatures)
            creature.update(merged)

        # Calculate modifiers
        for attr in ATTRIBUTES:
            creature[f"{attr}_mod"] = (creature[attr] - 10) // 2

    def _merge_type_attributes(
        self, creature: Dict[str, Any], types: List[str]
    ) -> None:
        """Merge attributes from creature types."""
        for creature_type in types:
            if creature_type not in self.base_creatures:
                continue

            base = self.base_creatures[creature_type]

            # Merge traits and keywords
            if "Traits" in base:
                traits = base["Traits"]
                for keyword, replacement in KEYWORDS.items():
                    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                    traits = pattern.sub(replacement, traits)
                creature["Traits"] = creature.get("Traits", "") + traits

            # Merge other attributes
            for attr in ["Actions", "Languages", "Speed", "Senses"]:
                if attr in base:
                    creature[attr] = creature.get(attr, "") + base[attr]

            # Handle meta traits
            if "meta" in base and "meta" not in creature:
                creature["meta"] = base["meta"]

    def _apply_color_traits(self, creature: Dict[str, Any], card: Dict[str, Any]) -> None:
        """Apply color traits based on card watermark."""
        if "watermark" in card:
            watermark = card["watermark"]
            watermark_key = "".join(watermark).lower()
            if watermark_key in COLOR_TRAITS:
                creature["Traits"] = (
                    creature.get("Traits", "") + COLOR_TRAITS[watermark_key]
                )

    def _apply_color_traits_from_list(self, creature: Dict[str, Any], color_trait_list: List[str]) -> None:
        """Apply color traits from a pre-filtered list (respects budget limits)."""
        from config import COLOR_TRAIT_BALANCE
        
        for trait_name in color_trait_list:
            if trait_name in COLOR_TRAIT_BALANCE:
                # Look up the HTML block for this color trait
                # The HTML is stored in COLOR_TRAITS dict
                trait_key = trait_name.lower()
                if trait_key in COLOR_TRAITS:
                    creature["Traits"] = (
                        creature.get("Traits", "") + COLOR_TRAITS[trait_key]
                    )

    def _extract_keywords_from_card(self, card: Dict[str, Any]) -> List[str]:
        """Extract MTG keywords from card oracle text."""
        from config import KEYWORDS
        
        keywords = []
        oracle_text = (card.get("oracle_text", "") or "").lower()
        
        # Check each keyword against oracle text
        for keyword in KEYWORDS.keys():
            keyword_lower = keyword.lower()
            # Simple keyword matching (can be enhanced with regex)
            if keyword_lower in oracle_text:
                keywords.append(keyword)
        
        return keywords

    def _extract_color_traits(self, card: Dict[str, Any]) -> List[str]:
        """Extract guild/color traits from card colors."""
        color_map = {
            ("W", "U"): "azorius",
            ("U", "B"): "dimir",
            ("B", "R"): "rakdos",
            ("B", "G"): "golgari",
            ("G", "W"): "selesnya",
            ("W", "B"): "orzhov",
            ("U", "R"): "izzet",
            ("R", "G"): "gruul",
            ("R", "W"): "boros",
            ("U", "G"): "simic",
        }
        
        colors = tuple(sorted(card.get("colors", [])))
        traits = []
        
        if colors in color_map:
            traits.append(color_map[colors])
        
        return traits



    def _apply_keyword_traits(self, creature: Dict[str, Any], keywords: List[str]) -> None:
        """Apply keyword trait HTML to creature traits."""
        for keyword in keywords:
            if keyword in KEYWORDS:
                creature["Traits"] = (
                    creature.get("Traits", "") + KEYWORDS[keyword]
                )


