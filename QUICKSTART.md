"""
Quick Start Guide for MTG Creatures Refactored

This guide will help you get started with the refactored MTG to D&D conversion pipeline.
"""

# ============================================================================
# INSTALLATION & SETUP
# ============================================================================

# 1. Ensure Python 3.8+ is installed
# python --version

# 2. No external dependencies needed - uses only stdlib modules:
#    - json, math, fractions, re (data processing)
#    - logging, pathlib, typing (utilities)

# 3. Place input files in the project root:
#    - monsters.json (base D&D creatures)
#    - ravnicaCreatures.json (MTG cards)


# ============================================================================
# RUNNING THE PIPELINE
# ============================================================================

# Basic execution:
# python main.py

# The pipeline will:
# 1. Load base monsters from monsters.json
# 2. Process and save to finalMonsters.json
# 3. Load Ravnica cards from ravnicaCreatures.json
# 4. Convert each card to D&D creature
# 5. Save results to final.json
# 6. Log new types discovered to newTypes.txt


# ============================================================================
# CONFIGURATION
# ============================================================================

# Most configuration is in config.py

# To change input/output files:
# config.py:
#   INPUT_MONSTERS_FILE = "path/to/your/monsters.json"
#   OUTPUT_RAVNICA_FILE = "path/to/output.json"

# To add new keywords:
# config.py:
#   KEYWORDS = {
#       "MyNewKeyword": "<property-block>...</property-block>",
#   }

# To add color traits:
# config.py:
#   COLOR_TRAITS = {
#       "mycolor": "<property-block>...</property-block>",
#   }

# To modify challenge ratings:
# config.py:
#   CHALLENGE_RATINGS = {
#       "3": {"Challenge": "3 (700 XP)", "Armor Class": 14, ...}
#   }


# ============================================================================
# UNDERSTANDING THE MODULES
# ============================================================================

"""
Module Responsibilities:

config.py
  - All static data and configuration
  - Add new traits, keywords, and challenge ratings here
  - File paths are defined here

file_utils.py
  - Loading/saving JSON files
  - Error handling for file operations
  - Caching layer to reduce disk I/O
  - Use: load_json(), save_json(), append_to_file()

stats_calculator.py
  - D&D-specific calculations
  - Ability score modifiers
  - Challenge rating calculations
  - Use: StatBlockCalculator class for stat operations

creature_converter.py
  - Core conversion logic
  - MonsterProcessor - processes base D&D monsters
  - RavnicaCardConverter - converts MTG cards
  - Use: Import and instantiate for custom conversions

main.py
  - Pipeline orchestration
  - Entry point for the application
  - Handles logging and error management
  - Use: Run directly or import for programmatic use
"""


# ============================================================================
# COMMON TASKS
# ============================================================================

# TASK 1: Process only monsters (skip cards)
# --------
# from file_utils import load_json, save_json
# from creature_converter import MonsterProcessor
# 
# creatures = load_json("monsters.json")
# processor = MonsterProcessor()
# processed = processor.process_monsters(creatures)
# save_json(processed, "output.json")


# TASK 2: Convert cards with custom configuration
# --------
# from creature_converter import RavnicaCardConverter
# from file_utils import load_json, save_json
# 
# base_creatures = load_json("finalMonsters.json")
# cards = load_json("ravnicaCreatures.json")
# 
# converter = RavnicaCardConverter(base_creatures)
# converted = converter.convert_cards(cards)
# save_json(converted, "output.json")


# TASK 3: Calculate CR for a specific card
# --------
# from stats_calculator import StatBlockCalculator
# from config import RARITY_MULTIPLIERS
# 
# rarity = "rare"
# cmc = 5.0  # converted mana cost
# power_toughness = 8.0  # power + toughness
# 
# multiplier = RARITY_MULTIPLIERS[rarity]
# cr = StatBlockCalculator.calculate_ravnica_card_cr(
#     multiplier, cmc, power_toughness
# )
# print(f"Calculated CR: {cr}")


# TASK 4: Adjust logging level for debugging
# --------
# import logging
# 
# # In your code before running:
# logging.basicConfig(level=logging.DEBUG)  # More verbose
# logging.basicConfig(level=logging.WARNING)  # Less verbose


# TASK 5: Extend with custom creature types
# --------
# In config.py, add to CREATURE_TYPES:
#   "MyCustomType"
# 
# Or dynamically:
#   from config import CREATURE_TYPES
#   CREATURE_TYPES.append("MyCustomType")


# ============================================================================
# LOGGING & DEBUGGING
# ============================================================================

# The application logs all operations. Check the output for:
# - [INFO] - Normal operation milestones
# - [WARNING] - Unexpected situations but not critical
# - [ERROR] - Something went wrong but recovered
# - [EXCEPTION] - Fatal error with full traceback

# To see more detailed logging:
# python main.py  2>&1 | tee output.log

# Common issues and solutions:

# Issue: "Cannot find monsters.json"
# Solution: Ensure monsters.json exists in the project root
#           Check file paths in config.py

# Issue: "Unknown CR X for creature Y"
# Solution: The creature has a CR value not in CHALLENGE_RATINGS
#           Add the missing CR to config.py or adjust baseline

# Issue: Low performance on large datasets
# Solution: The JSON cache may help, but for very large files:
#           - Consider chunking the input
#           - Use asyncio for I/O operations
#           - Profile with: python -m cProfile main.py


# ============================================================================
# EXTENDING THE PIPELINE
# ============================================================================

# EXTEND WITH CUSTOM PROCESSOR:
#
# from creature_converter import MonsterProcessor
# 
# class MyCustomProcessor(MonsterProcessor):
#     def process_monsters(self, creatures):
#         # Your custom logic
#         result = super().process_monsters(creatures)
#         # Additional processing
#         return result


# EXTEND WITH CUSTOM CONVERTER:
#
# from creature_converter import RavnicaCardConverter
# 
# class MyCustomConverter(RavnicaCardConverter):
#     def _convert_single_card(self, card):
#         creature = super()._convert_single_card(card)
#         # Your custom transformations
#         return creature


# ADD NEW CALCULATION:
#
# In stats_calculator.py:
#
# @staticmethod
# def my_custom_calculation(input_value: float) -> int:
#     """Calculate something custom."""
#     return int(input_value * some_factor)


# ============================================================================
# TESTING
# ============================================================================

# Test individual modules:

# Test config:
# import config
# assert len(config.CHALLENGE_RATINGS) == 31
# assert "STR" in config.ATTRIBUTES

# Test file_utils:
# from file_utils import load_json
# data = load_json("monsters.json")
# assert isinstance(data, list)

# Test stats_calculator:
# from stats_calculator import StatBlockCalculator
# cr = StatBlockCalculator.calculate_ravnica_card_cr(2, 4.0, 6.0)
# assert isinstance(cr, int)

# Test creature_converter:
# from creature_converter import MonsterProcessor
# processor = MonsterProcessor()
# assert processor is not None


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

# 1. Cache JSON loads:
#    Use load_json_cached() for frequently accessed files

# 2. Process sequentially first:
#    Ensure correctness before optimizing with async

# 3. Monitor memory:
#    Large datasets should be chunked and processed incrementally

# 4. Profile critical sections:
#    use cProfile to find bottlenecks

# 5. Clear cache when memory limited:
#    from file_utils import clear_cache
#    clear_cache()


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Problem: "ModuleNotFoundError: No module named 'config'"
# Solution: Ensure all .py files are in the same directory
#           Or add the directory to Python path:
#           import sys; sys.path.insert(0, 'path/to/project')

# Problem: Generated creatures have incomplete stats
# Solution: Check that all base creatures are processed first
#           Verify creature types are in CREATURE_TYPES
#           Check logs for "Unknown CR" warnings

# Problem: Script runs but produces empty output
# Solution: Verify input JSON files are valid
#           Check that card data has required fields
#           Enable DEBUG logging to see what's happening

# Problem: Out of memory on large datasets
# Solution: Process cards in batches instead of all at once
#           Implement streaming JSON parser
#           Clear processed cards from memory after saving


# ============================================================================
# WHERE TO GO NEXT
# ============================================================================

# 1. Read REFACTORING_GUIDE.md for architecture details
# 2. Read CHANGELOG.md to understand what changed
# 3. Check module docstrings for detailed API documentation
# 4. Examine test cases for usage examples (when added)
# 5. Review config.py to understand available configuration
# 6. Check creature_converter.py for conversion logic details

# ============================================================================
