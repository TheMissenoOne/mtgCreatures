"""Creature processing and conversion logic."""

import logging
import re
from fractions import Fraction
from typing import Any, Dict, List, Optional

from config import (
    ATTRIBUTES,
    CHALLENGE_RATINGS,
    COLOR_TRAITS,
    KEYWORDS,
    RARITY_MULTIPLIERS,
)
from stats_calculator import (
    StatBlockCalculator,
    apply_trait_adjustments,
    get_cr_from_challenge,
    parse_armor_class,
    parse_hit_points,
)
from file_utils import append_to_file

logger = logging.getLogger(__name__)

# Pre-compiled word-boundary patterns for keyword matching (built once at import)
_KEYWORD_PATTERNS: Dict[str, re.Pattern] = {
    kw: re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
    for kw in KEYWORDS
}

# Semantic oracle-text → keyword inference (pattern, keyword_name)
_ORACLE_INFERENCES = [
    (re.compile(r"can't be destroyed", re.IGNORECASE), "Indestructible"),
    (re.compile(r"can't be the target of spells or abilities", re.IGNORECASE), "Hexproof"),
    (re.compile(r"deals damage to a player,? you gain that much life", re.IGNORECASE), "Lifelink"),
    (re.compile(r"whenever .{0,30} deals damage,? .{0,20} gains? .{0,10} life", re.IGNORECASE), "Lifelink"),
    (re.compile(r"any amount of damage .{0,10} destroys", re.IGNORECASE), "Deathtouch"),
    (re.compile(r"can't be blocked except by", re.IGNORECASE), "Menace"),
]

# Single-color trait map
_MONO_COLOR_MAP = {
    ("W",): "white",
    ("U",): "blue",
    ("B",): "black",
    ("R",): "red",
    ("G",): "green",
}

# Dual-color guild map
_GUILD_COLOR_MAP = {
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


class MonsterProcessor:
    """Processes base monster data from D&D sources."""

    def __init__(self, new_types_file: str = "newTypes.txt"):
        self.new_types_file = new_types_file

    def process_monsters(
        self, creatures: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Process monster list and calculate relative modifiers."""
        processed = {}

        for creature in creatures:
            try:
                cr = get_cr_from_challenge(creature.get("Challenge", "0"))

                if cr not in CHALLENGE_RATINGS:
                    logger.warning(
                        "Unknown CR %s for creature %s", cr, creature.get("name")
                    )
                    continue

                creature_copy = creature.copy()
                creature_copy["Armor Class"] = parse_armor_class(
                    creature_copy["Armor Class"]
                )
                creature_copy["Hit Points"] = parse_hit_points(
                    creature_copy["Hit Points"]
                )

                for attr in ATTRIBUTES:
                    base_score = int(float(creature_copy.get(attr, 10)))
                    expected_base = 10 + Fraction(cr) * Fraction(3, 4)
                    modifier = int(base_score - expected_base)
                    creature_copy[f"{attr}_mod"] = modifier
                    creature_copy[attr] = 10 + modifier

                baseline = CHALLENGE_RATINGS[cr]
                creature_copy["Armor Class"] = (
                    baseline["Armor Class"] - creature_copy["Armor Class"]
                )
                creature_copy["Hit Points"] = int(creature_copy["Hit Points"])

                processed[creature_copy["name"]] = creature_copy

            except Exception as exc:
                logger.error(
                    "Error processing creature %s: %s", creature.get("name"), exc
                )
                continue

        logger.info("Processed %d monsters", len(processed))
        return processed


class RavnicaCardConverter:
    """Converts Magic: The Gathering Ravnica cards to D&D 5e creatures."""

    def __init__(self, base_creatures: Dict[str, Any]):
        self.base_creatures = base_creatures
        self.new_types: set = set()

        # Optional semantic matcher (requires scikit-learn)
        try:
            from creature_matcher import CreatureMatcher
            self.matcher: Optional[object] = CreatureMatcher(base_creatures)
        except Exception as exc:
            logger.warning("CreatureMatcher unavailable: %s", exc)
            self.matcher = None

    def convert_cards(self, cards: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Convert MTG cards to D&D creatures."""
        converted = {}

        valid_cards = [
            card
            for card in cards
            if (
                card.get("toughness", "").isnumeric()
                and card.get("power", "").isnumeric()
                and (float(card.get("power", 0)) + float(card.get("toughness", 0))) > 0
            )
        ]

        logger.info("Converting %d valid cards", len(valid_cards))

        for i, card in enumerate(valid_cards):
            if (i + 1) % max(1, len(valid_cards) // 10) == 0:
                logger.debug("Processed %d/%d cards", i + 1, len(valid_cards))

            try:
                creature = self._convert_single_card(card)
                if creature:
                    converted[creature["name"]] = creature
            except Exception as exc:
                logger.error("Error converting card %s: %s", card.get("name"), exc)
                continue

        logger.info("Converted %d creatures", len(converted))
        return converted

    def _convert_single_card(self, card: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Convert a single MTG card to a D&D creature stat block."""
        creature = card.copy()

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

        types = self._extract_creature_types(card)
        keywords = self._extract_keywords_from_card(card)
        creature_cr = self._calculate_creature_cr(card, types, len(keywords))

        if str(creature_cr) in CHALLENGE_RATINGS:
            creature.update(CHALLENGE_RATINGS[str(creature_cr)])

        self._calculate_abilities(creature, creature_cr, types, card)
        self._merge_type_attributes(creature, types)

        if "flavor_text" in card:
            creature["description"] = card["flavor_text"]

        color_traits = self._extract_color_traits(card)

        adjusted_creature = apply_trait_adjustments(
            creature, creature_cr, keywords, color_traits
        )
        creature.update(adjusted_creature)

        applied_keywords = adjusted_creature.get("_applied_keywords", [])
        applied_color_traits = adjusted_creature.get("_applied_color_traits", [])

        self._apply_keyword_traits(creature, applied_keywords)
        self._apply_color_traits_from_list(creature, applied_color_traits)

        from stats_calculator import apply_action_scaling, apply_defensive_budgets

        creature.update(apply_action_scaling(creature, creature_cr))
        creature.update(apply_defensive_budgets(creature, creature_cr))

        creature.pop("_applied_keywords", None)
        creature.pop("_applied_color_traits", None)

        return creature

    # ------------------------------------------------------------------
    # Type extraction
    # ------------------------------------------------------------------

    def _extract_creature_types(self, card: Dict[str, Any]) -> List[str]:
        """Extract D&D-valid creature type keys from card type line and name.

        Uses the semantic matcher to bridge unknown MTG types to D&D creature names.
        """
        raw_types: List[str] = []

        # Primary: subtypes from type_line (e.g., "Creature — Human Warrior" → ["Human", "Warrior"])
        type_line = card.get("type_line", "")
        if " — " in type_line:
            raw_types.extend(type_line.split(" — ")[1].split())

        # Fallback: words in card name
        for part in card.get("name", "").split():
            if part not in raw_types:
                raw_types.append(part)

        exact: List[str] = []
        unknown: List[str] = []

        for t in raw_types:
            if t in self.base_creatures:
                exact.append(t)
            else:
                self.new_types.add(t)
                unknown.append(t)

        # Semantic fallback for types not found by exact match
        semantic: List[str] = []
        if unknown and self.matcher is not None:
            semantic = self.matcher.find_matches_for_types(unknown, max_matches=2)
            # Only keep matches not already in exact
            semantic = [m for m in semantic if m not in exact]

        return list(dict.fromkeys(exact + semantic))  # deduplicate, preserve order

    # ------------------------------------------------------------------
    # CR calculation
    # ------------------------------------------------------------------

    def _calculate_creature_cr(
        self, card: Dict[str, Any], types: List[str], keyword_count: int = 0
    ) -> int:
        """Calculate base CR, adjusted by creature types and keyword complexity."""
        rarity = card.get("rarity", "common")
        cmc = float(card.get("cmc", 1))
        power = float(card.get("power", 0))
        toughness = float(card.get("toughness", 0))

        multiplier = RARITY_MULTIPLIERS.get(rarity, 1)

        base_cr = StatBlockCalculator.calculate_ravnica_card_cr(
            multiplier, cmc, power + toughness, keyword_count=keyword_count
        )

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

    # ------------------------------------------------------------------
    # Ability score calculation (improved)
    # ------------------------------------------------------------------

    def _calculate_abilities(
        self,
        creature: Dict[str, Any],
        cr: int,
        types: List[str],
        card: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Calculate differentiated ability scores from card characteristics.

        Uses P/T ratio, CMC, colors, and oracle keywords to push scores
        toward offensive (STR/DEX) or defensive (CON) profiles.
        """
        base = round(10 + Fraction(str(cr)) * Fraction(3, 4))
        scores = {attr: base for attr in ATTRIBUTES}

        if card is not None:
            power = float(card.get("power", 0))
            toughness = float(card.get("toughness", 0))
            cmc = float(card.get("cmc", 0))
            colors = card.get("colors", [])
            oracle = (card.get("oracle_text", "") or "").lower()
            pt_total = power + toughness

            # P/T ratio → STR vs CON split
            if pt_total > 0 and cr > 0:
                off_ratio = power / pt_total  # 0.0 = all toughness, 1.0 = all power
                delta = round((off_ratio - 0.5) * cr * 0.5)
                scores["STR"] = max(3, base + delta)
                scores["CON"] = max(3, base - delta)
                # Highly offensive cards get a slight DEX boost
                if off_ratio > 0.65:
                    scores["DEX"] = max(3, base + max(1, delta - 1))

            # High CMC → INT (complex spells/abilities)
            if cmc >= 4:
                scores["INT"] = base + min(4, round((cmc - 3) * 0.6))

            # Color-based adjustments
            if "W" in colors:
                scores["WIS"] = max(scores["WIS"], base + 2)
            if "U" in colors:
                scores["INT"] = max(scores["INT"], base + 3)
            if "B" in colors:
                scores["CHA"] = max(scores["CHA"], base + 2)
            if "G" in colors:
                scores["CON"] = max(scores["CON"], base + 1)
                scores["WIS"] = max(scores["WIS"], base + 1)
            # Red adds fury; slight STR/DEX
            if "R" in colors:
                scores["STR"] = max(scores["STR"], base + 1)

            # Oracle-text keyword hints
            if re.search(r"\bflying\b", oracle):
                scores["DEX"] = max(scores["DEX"], base + 2)
            if re.search(r"\btrample\b", oracle):
                scores["STR"] = max(scores["STR"], base + 2)
            if re.search(r"\bhexproof\b|\bindestructible\b", oracle):
                scores["CON"] = max(scores["CON"], base + 2)
            if re.search(r"\bmenace\b|\bfear\b|\bintimid", oracle):
                scores["CHA"] = max(scores["CHA"], base + 1)
            if re.search(r"\bscry\b|\bsurveil\b|\bsearch your library\b", oracle):
                scores["WIS"] = max(scores["WIS"], base + 1)
            if re.search(r"\bdraw a card\b|\bcounter target\b", oracle):
                scores["INT"] = max(scores["INT"], base + 1)

        # Write clamped pre-merge scores
        for attr in ATTRIBUTES:
            creature[attr] = min(30, max(1, scores[attr]))

        # Merge with type-based scores (average across matched D&D templates)
        type_creatures = [
            self.base_creatures[t] for t in types if t in self.base_creatures
        ]
        if type_creatures:
            merged = StatBlockCalculator.merge_stats_from_types(creature, type_creatures)
            creature.update(merged)

        # Apply P/T adjustment POST-merge so the signal isn't diluted away
        if card is not None and pt_total > 0:
            off_ratio = power / pt_total
            # Boost STR for offensive cards, CON for defensive ones
            if off_ratio >= 0.70:
                creature["STR"] = min(30, creature.get("STR", base) + 3)
                creature["CON"] = max(3, creature.get("CON", base) - 1)
                if off_ratio >= 0.80:
                    creature["DEX"] = min(30, creature.get("DEX", base) + 2)
            elif off_ratio <= 0.30:
                creature["CON"] = min(30, creature.get("CON", base) + 3)
                creature["STR"] = max(3, creature.get("STR", base) - 1)

        # Recalculate modifiers
        for attr in ATTRIBUTES:
            creature[f"{attr}_mod"] = (creature[attr] - 10) // 2

    # ------------------------------------------------------------------
    # Type attribute merging
    # ------------------------------------------------------------------

    def _merge_type_attributes(
        self, creature: Dict[str, Any], types: List[str]
    ) -> None:
        """Merge Traits/Actions/Languages/Speed from matched D&D base creatures."""
        for creature_type in types:
            if creature_type not in self.base_creatures:
                continue

            base = self.base_creatures[creature_type]

            if "Traits" in base:
                traits = base["Traits"]
                for keyword, replacement in KEYWORDS.items():
                    traits = re.sub(re.escape(keyword), replacement, traits, flags=re.IGNORECASE)
                creature["Traits"] = creature.get("Traits", "") + traits

            for attr in ["Actions", "Languages", "Speed", "Senses"]:
                if attr in base:
                    creature[attr] = creature.get(attr, "") + base[attr]

            if "meta" in base and not creature.get("meta"):
                creature["meta"] = base["meta"]

    # ------------------------------------------------------------------
    # Keyword extraction (improved)
    # ------------------------------------------------------------------

    def _extract_keywords_from_card(self, card: Dict[str, Any]) -> List[str]:
        """Extract D&D keyword mappings from card data.

        Priority:
        1. Explicit *keywords* field (Scryfall API)
        2. Word-boundary regex on oracle_text
        3. Semantic inference from oracle text patterns
        """
        found: set = set()

        # 1. Explicit keywords list (most reliable)
        for kw in card.get("keywords", []):
            kw_title = kw.title()
            if kw in KEYWORDS:
                found.add(kw)
            elif kw_title in KEYWORDS:
                found.add(kw_title)

        # 2. Word-boundary regex on oracle text
        oracle = card.get("oracle_text", "") or ""
        for keyword, pattern in _KEYWORD_PATTERNS.items():
            if pattern.search(oracle):
                found.add(keyword)

        # 3. Semantic inference
        oracle_lower = oracle.lower()
        for pattern, keyword in _ORACLE_INFERENCES:
            if keyword in KEYWORDS and pattern.search(oracle_lower):
                found.add(keyword)

        return list(found)

    # ------------------------------------------------------------------
    # Color trait extraction (mono + dual)
    # ------------------------------------------------------------------

    def _extract_color_traits(self, card: Dict[str, Any]) -> List[str]:
        """Map card colors to guild or mono-color trait keys."""
        colors = tuple(sorted(card.get("colors", [])))

        if colors in _GUILD_COLOR_MAP:
            return [_GUILD_COLOR_MAP[colors]]
        if colors in _MONO_COLOR_MAP:
            return [_MONO_COLOR_MAP[colors]]
        return []

    # ------------------------------------------------------------------
    # Trait HTML application
    # ------------------------------------------------------------------

    def _apply_keyword_traits(
        self, creature: Dict[str, Any], keywords: List[str]
    ) -> None:
        for keyword in keywords:
            if keyword in KEYWORDS:
                creature["Traits"] = creature.get("Traits", "") + KEYWORDS[keyword]

    def _apply_color_traits_from_list(
        self, creature: Dict[str, Any], color_trait_list: List[str]
    ) -> None:
        for trait_name in color_trait_list:
            key = trait_name.lower()
            if key in COLOR_TRAITS:
                creature["Traits"] = creature.get("Traits", "") + COLOR_TRAITS[key]

    def _apply_color_traits(
        self, creature: Dict[str, Any], card: Dict[str, Any]
    ) -> None:
        """Legacy watermark-based trait application (kept for compatibility)."""
        if "watermark" in card:
            watermark_key = "".join(card["watermark"]).lower()
            if watermark_key in COLOR_TRAITS:
                creature["Traits"] = creature.get("Traits", "") + COLOR_TRAITS[watermark_key]
