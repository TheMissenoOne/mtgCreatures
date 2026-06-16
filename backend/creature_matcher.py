"""Semantic base-creature matching using TF-IDF cosine similarity.

Finds the best D&D 5e monster match for a given MTG creature type string.
Fallback hierarchy: exact → category → word-overlap → fuzzy → TF-IDF.
"""

import difflib
import logging
import re
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available — TF-IDF matching disabled, using fuzzy only")


# MTG type → candidate D&D creature name fragments (lowercase)
_TYPE_CATEGORY_MAP: Dict[str, List[str]] = {
    # Humanoids
    "human":      ["bandit", "guard", "soldier", "knight"],
    "elf":        ["elf", "drow"],
    "dwarf":      ["dwarf"],
    "goblin":     ["goblin"],
    "orc":        ["orc"],
    "gnome":      ["gnome"],
    "kobold":     ["kobold"],
    # Undead
    "zombie":     ["zombie"],
    "skeleton":   ["skeleton"],
    "ghost":      ["ghost", "specter"],
    "vampire":    ["vampire"],
    "lich":       ["lich"],
    "shade":      ["shadow", "specter", "wraith"],
    "specter":    ["specter"],
    "wraith":     ["wraith"],
    # Beasts
    "wolf":       ["wolf", "worg"],
    "bear":       ["brown bear"],
    "snake":      ["constrictor snake"],
    "bird":       ["giant eagle", "hawk"],
    "spider":     ["spider"],
    "rat":        ["rat"],
    "cat":        ["lion", "panther"],
    "horse":      ["warhorse"],
    "boar":       ["boar"],
    "crocodile":  ["crocodile"],
    # Dragons & scaled
    "dragon":     ["dragon"],
    "drake":      ["wyvern", "dragon"],
    "wyrm":       ["dragon"],
    "serpent":    ["giant constrictor snake"],
    "basilisk":   ["basilisk"],
    "cockatrice": ["cockatrice"],
    "hydra":      ["hydra"],
    "wyvern":     ["wyvern"],
    # Giants
    "giant":      ["giant"],
    "troll":      ["troll"],
    "ogre":       ["ogre"],
    "cyclops":    ["cyclops"],
    "titan":      ["titan"],
    # Magical / celestials
    "angel":      ["angel", "deva", "planetar"],
    "demon":      ["demon"],
    "devil":      ["devil"],
    "elemental":  ["elemental"],
    "sphinx":     ["sphinx"],
    "faerie":     ["sprite", "pixie"],
    "archon":     ["deva", "planetar", "solar"],
    "praetor":    ["pit fiend", "balor"],
    "hellion":    ["balor", "pit fiend"],
    # Aquatic
    "merfolk":    ["merrow"],
    "leviathan":  ["kraken"],
    "fish":       ["quipper"],
    "crab":       ["giant crab"],
    "octopus":    ["giant octopus"],
    # Constructs
    "golem":      ["golem"],
    "homunculus": ["homunculus"],
    # Plants & fungi
    "plant":      ["vine blight"],
    "fungus":     ["violet fungus"],
    "treefolk":   ["treant"],
    # Ravnica-specific types
    "viashino":   ["lizardfolk"],
    "vedalken":   ["archmage"],
    "nephilim":   ["tarrasque"],
    "thrull":     ["ghoul"],
    "jellyfish":  ["sea spawn"],
    "wurm":       ["purple worm"],
    "griffin":    ["griffon"],
    "mutant":     ["gibbering mouther"],
    "shapeshifter": ["doppelganger"],
    "dinosaur":   ["tyrannosaurus rex", "triceratops"],
    "phoenix":    ["roc"],
    "shaman":     ["druid"],
    "wizard":     ["mage", "archmage"],
    "cleric":     ["priest"],
    "warrior":    ["veteran", "gladiator"],
    "soldier":    ["veteran"],
    "assassin":   ["assassin"],
    "scout":      ["scout"],
    "berserker":  ["berserker"],
    "monk":       ["monk"],
    "ranger":     ["ranger"],
    "rogue":      ["spy", "assassin"],
}


class CreatureMatcher:
    """Matches MTG creature type strings to D&D base creature entries."""

    def __init__(self, base_creatures: Dict[str, Any]):
        self.base_creatures = base_creatures
        self.names: List[str] = list(base_creatures.keys())
        self._names_lower: List[str] = [n.lower() for n in self.names]
        self._tfidf_ready = False

        if _SKLEARN_AVAILABLE and self.names:
            self._build_index()

    def _creature_doc(self, name: str, creature: Dict[str, Any]) -> str:
        """Build search text from creature name + meta (type line)."""
        meta = creature.get("meta", "")
        # Strip HTML tags from traits for richer vocabulary
        traits_raw = creature.get("Traits", "")[:200]
        traits_clean = re.sub(r"<[^>]+>", " ", traits_raw)
        return f"{name} {meta} {traits_clean}".lower()

    def _build_index(self) -> None:
        """Build TF-IDF index over all base creature documents."""
        try:
            corpus = [
                self._creature_doc(name, self.base_creatures[name])
                for name in self.names
            ]
            self._vectorizer = TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2),
                max_features=8000,
                sublinear_tf=True,
            )
            self._matrix = self._vectorizer.fit_transform(corpus)
            self._tfidf_ready = True
            logger.info("CreatureMatcher: TF-IDF index ready (%d entries)", len(self.names))
        except Exception as exc:
            logger.warning("CreatureMatcher: index build failed: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def find_best_match(self, query: str, threshold: float = 0.08) -> Optional[str]:
        """Return the name of the best matching D&D creature for *query*.

        Returns None when no reasonable match is found.
        """
        q = query.strip().lower()
        if not q:
            return None

        # 1. Exact name match
        if q in self._names_lower:
            return self.names[self._names_lower.index(q)]

        # 2. Category map lookup (MTG type → known D&D candidate fragments)
        for type_key, candidates in _TYPE_CATEGORY_MAP.items():
            if type_key in q or q in type_key:
                for fragment in candidates:
                    for i, name_low in enumerate(self._names_lower):
                        if fragment in name_low:
                            return self.names[i]

        # 3. Single-word overlap
        q_words = set(q.split())
        best_name: Optional[str] = None
        best_overlap = 0
        for i, name_low in enumerate(self._names_lower):
            n_words = set(name_low.split())
            overlap = len(q_words & n_words)
            if overlap > best_overlap:
                best_overlap = overlap
                best_name = self.names[i]
        if best_overlap >= 1:
            return best_name

        # 4. Fuzzy string matching
        close = difflib.get_close_matches(q, self._names_lower, n=1, cutoff=0.6)
        if close:
            return self.names[self._names_lower.index(close[0])]

        # 5. TF-IDF cosine similarity
        if self._tfidf_ready:
            try:
                q_vec = self._vectorizer.transform([q])
                scores = cosine_similarity(q_vec, self._matrix)[0]
                best_idx = int(np.argmax(scores))
                if scores[best_idx] >= threshold:
                    return self.names[best_idx]
            except Exception as exc:
                logger.debug("CreatureMatcher: TF-IDF query error: %s", exc)

        return None

    def find_matches_for_types(
        self, types: List[str], max_matches: int = 3
    ) -> List[str]:
        """Return up to *max_matches* D&D creature names for a list of MTG types."""
        seen: set = set()
        results: List[str] = []
        for type_str in types:
            match = self.find_best_match(type_str)
            if match and match not in seen:
                results.append(match)
                seen.add(match)
                if len(results) >= max_matches:
                    break
        return results
