"""Main entry point for MTG to D&D conversion pipeline."""

import logging
import sys
from pathlib import Path

from config import (
    INPUT_MONSTERS_FILE,
    INPUT_RAVNICA_FILE,
    OUTPUT_MONSTERS_FILE,
    OUTPUT_RAVNICA_FILE,
    NEW_TYPES_LOG_FILE,
)
from file_utils import load_json, save_json, append_to_file
from creature_converter import MonsterProcessor, RavnicaCardConverter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def process_base_monsters() -> dict:
    """
    Process base monster data and save to file.
    
    Returns:
        Dictionary of processed monsters
    """
    logger.info("=" * 60)
    logger.info("STAGE 1: Processing base monsters")
    logger.info("=" * 60)
    
    try:
        creatures = load_json(INPUT_MONSTERS_FILE)
        logger.info(f"Loaded {len(creatures)} base creatures from {INPUT_MONSTERS_FILE}")
    except FileNotFoundError:
        logger.error(f"Cannot find {INPUT_MONSTERS_FILE}")
        return {}

    processor = MonsterProcessor(NEW_TYPES_LOG_FILE)
    processed = processor.process_monsters(creatures)

    save_json(processed, OUTPUT_MONSTERS_FILE)
    logger.info(f"Saved {len(processed)} processed monsters to {OUTPUT_MONSTERS_FILE}")
    
    return processed


def process_ravnica_cards(base_creatures: dict) -> dict:
    """
    Convert Ravnica cards to D&D creatures.
    
    Args:
        base_creatures: Processed base creature data
        
    Returns:
        Dictionary of converted creatures
    """
    logger.info("=" * 60)
    logger.info("STAGE 2: Converting Ravnica cards")
    logger.info("=" * 60)
    
    try:
        cards = load_json(INPUT_RAVNICA_FILE)
        logger.info(f"Loaded {len(cards)} cards from {INPUT_RAVNICA_FILE}")
    except FileNotFoundError:
        logger.error(f"Cannot find {INPUT_RAVNICA_FILE}")
        return {}

    converter = RavnicaCardConverter(base_creatures)
    converted = converter.convert_cards(cards)

    # Log new creature types found
    if converter.new_types:
        logger.info(f"Found {len(converter.new_types)} new creature types")
        for new_type in sorted(converter.new_types):
            append_to_file(NEW_TYPES_LOG_FILE, new_type)

    save_json(converted, OUTPUT_RAVNICA_FILE)
    logger.info(f"Saved {len(converted)} creatures to {OUTPUT_RAVNICA_FILE}")
    
    return converted


def main():
    """Main pipeline execution."""
    logger.info("Starting MTG to D&D conversion pipeline")
    
    try:
        # Stage 1: Process base monsters
        base_creatures = process_base_monsters()
        if not base_creatures:
            logger.error("No base creatures processed. Aborting.")
            return 1

        # Stage 2: Convert Ravnica cards
        converted_creatures = process_ravnica_cards(base_creatures)
        if not converted_creatures:
            logger.warning("No Ravnica creatures converted")

        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info(f"Total creatures processed: {len(base_creatures) + len(converted_creatures)}")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.exception(f"Pipeline failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
