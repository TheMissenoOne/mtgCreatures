"""Scrape D&D 5e SRD bestiary data and convert to monsters.json format.

Primary source: 5e-bits/5e-database (SRD creatures, Creative Commons)
Alternative: 5e.tools bestiary JSON (requires local download due to site restrictions)

Usage:
  # Fetch from GitHub (SRD creatures):
  python scraper.py

  # Fetch a single source subset:
  python scraper.py --sources srd

  # Load locally downloaded 5e.tools JSON files:
  python scraper.py --local-dir data/source/5etools/

  # Custom output path:
  python scraper.py --output /path/to/output.json
"""

import argparse
import json
import logging
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Matches CHALLENGE_RATINGS in config.py
CR_XP = {
    "0": 10, "1/8": 25, "1/4": 50, "1/2": 100,
    "1": 200, "2": 450, "3": 700, "4": 1100,
    "5": 1800, "6": 2300, "7": 2900, "8": 3900,
    "9": 5000, "10": 5900, "11": 7200, "12": 8400,
    "13": 10000, "14": 11500, "15": 13000, "16": 15000,
    "17": 18000, "18": 20000, "19": 22000, "20": 25000,
    "21": 33000, "22": 41000, "23": 50000, "24": 62000,
    "25": 75000, "26": 90000, "27": 105000, "28": 120000,
    "29": 135000, "30": 155000,
}

_CR_FLOAT_TO_STR = {0.125: "1/8", 0.25: "1/4", 0.5: "1/2", 0: "0"}

# Remote sources (must be publicly accessible JSON)
BESTIARY_SOURCES = {
    "srd": "https://raw.githubusercontent.com/5e-bits/5e-database/main/src/2014/en/5e-SRD-Monsters.json",
}

# 5e.tools format constants (for local file support)
_5ET_SIZE_NAMES = {
    "T": "Tiny", "S": "Small", "M": "Medium",
    "L": "Large", "H": "Huge", "G": "Gargantuan",
}
_5ET_ALIGNMENT_MAP = {
    ("L", "G"): "lawful good", ("L", "N"): "lawful neutral", ("L", "E"): "lawful evil",
    ("N", "G"): "neutral good", ("N", "N"): "neutral", ("N", "E"): "neutral evil",
    ("C", "G"): "chaotic good", ("C", "N"): "chaotic neutral", ("C", "E"): "chaotic evil",
}
_5ET_ATK_TAGS = {
    "{@atk mw}": "Melee Weapon Attack:", "{@atk rw}": "Ranged Weapon Attack:",
    "{@atk mw,rw}": "Melee or Ranged Weapon Attack:", "{@atk ms}": "Melee Spell Attack:",
    "{@atk rs}": "Ranged Spell Attack:", "{@atk ms,rs}": "Melee or Ranged Spell Attack:",
}


# ---------------------------------------------------------------------------
# CR helpers
# ---------------------------------------------------------------------------

def float_cr_to_str(cr_float: float) -> str:
    """Convert a numeric CR (0.125, 0.5, 10, etc.) to string key."""
    if cr_float in _CR_FLOAT_TO_STR:
        return _CR_FLOAT_TO_STR[cr_float]
    return str(int(cr_float))


def build_challenge_string(cr_str: str, xp: int | None = None) -> str:
    """Build the Challenge field string, e.g. '1/4 (50 XP)'."""
    if cr_str not in CR_XP:
        cr_str = "0"
    xp_val = xp if xp is not None else CR_XP[cr_str]
    return f"{cr_str} ({xp_val} XP)"


# ---------------------------------------------------------------------------
# SRD format (5e-bits/5e-database) converter
# ---------------------------------------------------------------------------

def _srd_entries_to_html(entries: list, include_legendary: bool = False) -> str:
    """Convert SRD action/ability list (name+desc) to property-block HTML."""
    parts = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name", "")
        desc = entry.get("desc", "")
        if name and desc:
            parts.append(f'<property-block><h4>{name}.</h4><p>{desc}</p></property-block>')
    return "".join(parts)


def _srd_build_speed(speed: dict) -> str:
    """Convert SRD speed dict to speed string."""
    if not speed:
        return "30 ft."
    parts = []
    if "walk" in speed:
        parts.append(speed["walk"])
    for mode in ("burrow", "climb", "fly", "swim"):
        if mode in speed:
            val = speed[mode]
            if isinstance(val, dict):
                val = val.get("value", val.get("speed", "0 ft."))
            hover = " (hover)" if mode == "fly" and speed.get("hover") else ""
            parts.append(f"{mode} {val}{hover}")
    return ", ".join(parts) if parts else "30 ft."


def _srd_build_senses(senses: dict) -> str:
    """Convert SRD senses dict to senses string."""
    parts = []
    for sense, val in senses.items():
        if sense == "passive_perception":
            continue
        parts.append(f"{sense.replace('_', ' ')} {val}")
    passive = senses.get("passive_perception", 10)
    parts.append(f"passive Perception {passive}")
    return ", ".join(parts)


def _srd_extract_ac(ac_list: list) -> str:
    if not ac_list:
        return "10"
    first = ac_list[0]
    if isinstance(first, dict):
        return str(first.get("value", first.get("ac", 10)))
    return str(first)


def convert_srd_monster(raw: dict) -> dict | None:
    """Convert a 5e-bits SRD monster to monsters.json format."""
    name = raw.get("name", "").strip()
    if not name:
        return None

    cr_float = raw.get("challenge_rating", 0)
    cr_str = float_cr_to_str(float(cr_float))
    xp = raw.get("xp")
    challenge = build_challenge_string(cr_str, xp)

    hp = raw.get("hit_points", 4)
    hp_roll = raw.get("hit_points_roll") or raw.get("hit_dice", "1d8")
    hp_str = f"{hp} ({hp_roll})"

    size = raw.get("size", "Medium")
    creature_type = raw.get("type", "creature")
    subtype = raw.get("subtype", "")
    alignment = raw.get("alignment", "unaligned")
    meta = f"{size} {creature_type}"
    if subtype:
        meta += f" ({subtype})"
    meta += f", {alignment}"

    actions = _srd_entries_to_html(raw.get("actions", []))
    legendary = _srd_entries_to_html(raw.get("legendary_actions", []))
    if legendary:
        actions += legendary

    return {
        "name": name,
        "meta": meta,
        "Armor Class": _srd_extract_ac(raw.get("armor_class", [10])),
        "Hit Points": hp_str,
        "Speed": _srd_build_speed(raw.get("speed", {})),
        "STR": str(raw.get("strength", 10)),
        "DEX": str(raw.get("dexterity", 10)),
        "CON": str(raw.get("constitution", 10)),
        "INT": str(raw.get("intelligence", 10)),
        "WIS": str(raw.get("wisdom", 10)),
        "CHA": str(raw.get("charisma", 10)),
        "Senses": _srd_build_senses(raw.get("senses", {})),
        "Languages": raw.get("languages", "—") or "—",
        "Challenge": challenge,
        "Traits": _srd_entries_to_html(raw.get("special_abilities", [])),
        "Actions": actions,
    }


# ---------------------------------------------------------------------------
# 5e.tools format converter (for locally downloaded files)
# ---------------------------------------------------------------------------

def _5et_strip_tags(text: str) -> str:
    """Remove 5e.tools {@tag ...} syntax."""
    for tag, replacement in _5ET_ATK_TAGS.items():
        text = text.replace(tag, replacement)
    text = re.sub(r'\{@h\}', '', text)
    text = re.sub(r'\{@recharge (\d+)\}', r'(Recharge \1-6)', text)
    text = re.sub(r'\{@recharge\}', '(Recharge 6)', text)
    text = re.sub(r'\{@dc (\d+)\}', r'DC \1', text)
    text = re.sub(r'\{@hit ([+-]?\d+)\}', r'\1', text)
    text = re.sub(r'\{@(?:damage|dice|scaledice|scaledamage) ([^|}]+)(?:\|[^}]*)?\}', r'\1', text)
    text = re.sub(r'\{@\w+ ([^|}]+)\|[^}]*\}', r'\1', text)
    text = re.sub(r'\{@\w+ ([^}]+)\}', r'\1', text)
    text = re.sub(r'\{@\w+\}', '', text)
    return text.strip()


def _5et_flatten(entry: Any) -> str:
    if isinstance(entry, str):
        return _5et_strip_tags(entry)
    if isinstance(entry, dict):
        parts = [_5et_flatten(e) for e in entry.get("entries", [])]
        parts += ["• " + _5et_flatten(i) for i in entry.get("items", []) if isinstance(i, str)]
        return " ".join(p for p in parts if p)
    return ""


def _5et_entries_to_html(entries: list) -> str:
    parts = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name", "")
        text = " ".join(_5et_flatten(e) for e in entry.get("entries", [])).strip()
        if name and text:
            parts.append(f'<property-block><h4>{name}.</h4><p>{text}</p></property-block>')
    return "".join(parts)


def _5et_normalize_alignment(align: list) -> str:
    if not align:
        return "unaligned"
    if "U" in align:
        return "unaligned"
    if "A" in align:
        return "any alignment"
    if len(align) == 1:
        return {"L": "lawful", "N": "neutral", "C": "chaotic"}.get(align[0], "unaligned")
    if len(align) >= 2:
        return _5ET_ALIGNMENT_MAP.get((align[0], align[1]), "any alignment")
    return "any alignment"


def _5et_extract_cr(cr_field: Any) -> str:
    if isinstance(cr_field, str):
        return cr_field
    if isinstance(cr_field, (int, float)):
        return float_cr_to_str(float(cr_field))
    if isinstance(cr_field, dict):
        return str(cr_field.get("cr", "0"))
    return "0"


def _5et_extract_ac(ac_field: list) -> str:
    if not ac_field:
        return "10"
    first = ac_field[0]
    return str(first.get("ac", 10) if isinstance(first, dict) else first)


def _5et_extract_type(type_field: Any) -> tuple:
    if isinstance(type_field, str):
        return type_field, ""
    if isinstance(type_field, dict):
        tags = type_field.get("tags", [])
        return type_field.get("type", "creature"), ", ".join(str(t) for t in tags)
    return "creature", ""


def _5et_build_speed(speed: dict) -> str:
    if not speed:
        return "30 ft."

    def _val(v):
        return int(v.get("number", 0)) if isinstance(v, dict) else int(v or 0)

    walk = _val(speed.get("walk", 30))
    parts = [f"{walk} ft."]
    for mode in ("burrow", "climb", "fly", "swim"):
        if mode in speed:
            n = _val(speed[mode])
            if n > 0:
                hover = " (hover)" if mode == "fly" and speed.get("canHover") else ""
                parts.append(f"{mode} {n} ft.{hover}")
    return ", ".join(parts)


def convert_5etools_monster(raw: dict) -> dict | None:
    """Convert a 5e.tools bestiary monster to monsters.json format."""
    name = raw.get("name", "").strip()
    if not name:
        return None

    cr_str = _5et_extract_cr(raw.get("cr", "0"))
    if cr_str not in CR_XP:
        cr_str = "0"
    challenge = build_challenge_string(cr_str)

    hp_data = raw.get("hp", {})
    if isinstance(hp_data, dict):
        hp_str = f"{hp_data.get('average', 4)} ({hp_data.get('formula', '1d8')})"
    else:
        hp_str = f"{hp_data} (1d8)"

    size = _5ET_SIZE_NAMES.get(raw.get("size", "M"), "Medium")
    creature_type, subtype = _5et_extract_type(raw.get("type", ""))
    align = _5et_normalize_alignment(raw.get("alignment", []))
    meta = f"{size} {creature_type}" + (f" ({subtype})" if subtype else "") + f", {align}"

    senses = list(raw.get("senses", []))
    senses.append(f"passive Perception {raw.get('passive', 10)}")

    langs = raw.get("languages", [])
    languages = (", ".join(langs) if isinstance(langs, list) else langs) or "—"

    return {
        "name": name,
        "meta": meta,
        "Armor Class": _5et_extract_ac(raw.get("ac", [10])),
        "Hit Points": hp_str,
        "Speed": _5et_build_speed(raw.get("speed", {})),
        "STR": str(raw.get("str", 10)),
        "DEX": str(raw.get("dex", 10)),
        "CON": str(raw.get("con", 10)),
        "INT": str(raw.get("int", 10)),
        "WIS": str(raw.get("wis", 10)),
        "CHA": str(raw.get("cha", 10)),
        "Senses": ", ".join(senses),
        "Languages": languages,
        "Challenge": challenge,
        "Traits": _5et_entries_to_html(raw.get("trait", [])),
        "Actions": _5et_entries_to_html(raw.get("action", [])),
    }


# ---------------------------------------------------------------------------
# Fetch / load helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str) -> Any:
    """Download and parse JSON from a URL."""
    logger.info(f"Fetching {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_local_5etools_dir(directory: str) -> list:
    """Load all bestiary-*.json files from a local 5e.tools data directory."""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    raw_monsters = []
    for json_file in sorted(dir_path.glob("bestiary-*.json")):
        logger.info(f"Loading {json_file.name}")
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
        raw_monsters.extend(data.get("monster", []))
        logger.info(f"  Found {len(data.get('monster', []))} monsters")

    return raw_monsters


# ---------------------------------------------------------------------------
# Main scrape orchestration
# ---------------------------------------------------------------------------

def scrape_remote(sources: list, seen_names: set, out: list) -> None:
    """Fetch SRD sources from GitHub and convert."""
    for src in sources:
        url = BESTIARY_SOURCES.get(src)
        if not url:
            logger.warning(f"Unknown source '{src}'. Available: {', '.join(BESTIARY_SOURCES)}")
            continue
        try:
            raw_data = fetch_json(url)
        except Exception as exc:
            logger.error(f"Failed to fetch {src}: {exc}")
            continue

        monsters = raw_data if isinstance(raw_data, list) else raw_data.get("monster", [])
        logger.info(f"  {src}: {len(monsters)} monsters fetched")

        added = 0
        for raw in monsters:
            converted = convert_srd_monster(raw)
            if converted is None:
                continue
            if converted["name"] in seen_names:
                continue
            seen_names.add(converted["name"])
            out.append(converted)
            added += 1
        logger.info(f"  {src}: {added} creatures converted")


def scrape_local_5etools(local_dir: str, seen_names: set, out: list) -> None:
    """Load locally downloaded 5e.tools bestiary files and convert."""
    try:
        raw_monsters = load_local_5etools_dir(local_dir)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        return

    logger.info(f"local-5etools: {len(raw_monsters)} total monsters found")
    added = 0
    for raw in raw_monsters:
        converted = convert_5etools_monster(raw)
        if converted is None:
            continue
        if converted["name"] in seen_names:
            continue
        seen_names.add(converted["name"])
        out.append(converted)
        added += 1
    logger.info(f"local-5etools: {added} creatures converted")


def run_scraper(sources: list, output_path: str, local_dir: str | None = None) -> int:
    """Full scrape pipeline. Returns count of converted creatures."""
    all_creatures: list = []
    seen_names: set = set()

    if local_dir:
        scrape_local_5etools(local_dir, seen_names, all_creatures)

    if sources:
        scrape_remote(sources, seen_names, all_creatures)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(all_creatures, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved {len(all_creatures)} creatures to {output_path}")
    return len(all_creatures)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Scrape D&D 5e bestiary data and convert to monsters.json format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py                        # Fetch SRD creatures from GitHub
  python scraper.py --sources srd          # Same as above
  python scraper.py --local-dir data/source/5etools/  # Use local 5e.tools files
  python scraper.py --output /tmp/out.json # Custom output path
""",
    )
    parser.add_argument(
        "--sources",
        nargs="*",
        default=list(BESTIARY_SOURCES.keys()),
        metavar="SRC",
        help=f"Remote sources to fetch. Options: {', '.join(BESTIARY_SOURCES)}. Default: all.",
    )
    parser.add_argument(
        "--local-dir",
        default=None,
        metavar="DIR",
        help=(
            "Directory containing locally downloaded 5e.tools bestiary JSON files "
            "(bestiary-mm.json, bestiary-vgm.json, etc.). "
            "Download from https://5e.tools/data/bestiary/ in your browser."
        ),
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path. Default: data/source/monsters_5etools.json",
    )
    args = parser.parse_args()

    if args.output is None:
        project_root = Path(__file__).parent.parent
        args.output = str(project_root / "data" / "source" / "monsters_5etools.json")

    if not args.sources and not args.local_dir:
        parser.error("Provide --sources or --local-dir (or both).")

    count = run_scraper(args.sources, args.output, args.local_dir)
    return 0 if count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
