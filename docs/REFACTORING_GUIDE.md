# MTG Creatures - Refactored

## Overview
A refactored and modularized Python pipeline that converts Magic: The Gathering card data from Scryfall into Dungeons & Dragons 5th Edition creature stat blocks.

## Architecture

The project has been completely refactored from a single 492-line monolithic script into a clean, modular structure:

### Module Structure

```
mtgCreatures/
├── main.py                 # Entry point with pipeline orchestration
├── config.py              # Configuration and static data
├── file_utils.py          # File I/O operations with caching
├── stats_calculator.py    # D&D stat calculations and formulas
├── creature_converter.py  # Core conversion logic
├── monsters.json          # Base D&D monster data
├── ravnicaCreatures.json  # MTG card data
├── final.json            # Output: Converted creatures
└── finalMonsters.json    # Output: Processed base monsters
```

## Key Improvements

### 1. **Modularity**
- **config.py**: All static data (challenge ratings, keywords, color traits) separated into a single configuration module
- **file_utils.py**: Centralized file operations with error handling and caching
- **stats_calculator.py**: D&D stat calculations isolated into reusable functions
- **creature_converter.py**: Core conversion logic split into specialized classes

### 2. **Performance Improvements**
- **JSON Caching**: Eliminated repeated file I/O through `load_json_cached()` function
- **Optimized Loops**: Reduced nested loop complexity with pre-computed type lookups
- **Early Termination**: Skip invalid cards early to avoid unnecessary processing
- **Batch Operations**: Process cards in batches with progress logging

### 3. **Code Quality**
- **Type Hints**: Added Python type annotations for better IDE support and clarity
- **Documentation**: Comprehensive docstrings for all functions and classes
- **Error Handling**: Graceful error handling with logging throughout
- **Logging**: Structured logging with INFO, WARNING, and ERROR levels
- **Constants**: Magic numbers and strings moved to configuration

### 4. **Maintainability**
- **Single Responsibility**: Each module has a clear, focused purpose
- **Testability**: Functions and classes are now independently testable
- **Extensibility**: Easy to add new features or modify conversion logic
- **Configuration**: Static data easily modified without touching code logic

## Module Details

### `config.py`
Centralizes all configuration data:
- Challenge rating difficulty classes (CR 0-30)
- D&D ability scores (STR, DEX, CON, INT, WIS, CHA)
- MTG creature types for lookups
- Color/Guild trait translations (Azorius, Dimir, etc.)
- MTG keywords mapped to D&D abilities
- Rarity multipliers
- File paths

### `file_utils.py`
File operations with best practices:
- `load_json()` - Load with error handling
- `save_json()` - Save with optional formatting
- `append_to_file()` - Append new types discovered
- `load_json_cached()` - Caching layer to reduce disk I/O
- `clear_cache()` - Cache management

### `stats_calculator.py`
D&D specific calculations:
- `parse_armor_class()` - Handle string/int AC values
- `parse_hit_points()` - Handle string/int HP values
- `calculate_ability_modifier()` - D&D modifier formula
- `StatBlockCalculator` class with:
  - `calculate_creature_stats_from_baseline()` - Compute stat adjustments
  - `merge_stats_from_types()` - Average traits across multiple types
  - `calculate_ravnica_card_cr()` - CR calculation from MTG metrics

### `creature_converter.py`
Core conversion logic:
- `MonsterProcessor` - Converts base D&D monsters to modular stats
- `RavnicaCardConverter` - Converts MTG cards to D&D creatures
  - `convert_cards()` - Batch card conversion
  - `_extract_creature_types()` - Parse card names/types
  - `_calculate_creature_cr()` - Compute CR with type adjustments
  - `_calculate_abilities()` - Derive ability scores
  - `_merge_type_attributes()` - Combine type traits/actions
  - `_apply_color_traits()` - Add color/guild abilities

### `main.py`
Pipeline orchestration:
- `process_base_monsters()` - Stage 1: Process D&D sources
- `process_ravnica_cards()` - Stage 2: Convert MTG cards
- `main()` - Unified pipeline with error handling
- Structured logging with clear progress indicators

## Performance Metrics

### Before Refactoring
- Sequential file I/O in inner loops
- O(n²) lookups with dictionary checks
- No error handling  or logging
- Difficult to profile bottlenecks

### After Refactoring
- **JSON Caching**: Eliminated redundant file loads from nested loops
- **Pre-computed Lookups**: Type creatures cached for O(1) access
- **Early Filtering**: Invalid cards excluded before processing
- **Structured Logging**: Identify and address bottlenecks easily
- **Progress Monitoring**: ~10% progress markers for long-running operations

## Usage

```bash
python main.py
```

The script will:
1. Load base monsters from `monsters.json`
2. Calculate and save processed stats to `finalMonsters.json`
3. Load Ravnica cards from `ravnicaCreatures.json`
4. Convert each valid card to a D&D creature
5. Save results to `final.json`
6. Log any new creature types discovered to `newTypes.txt`

## Configuration

To modify behavior:

**Change file paths** in `config.py`:
```python
INPUT_MONSTERS_FILE = "path/to/monsters.json"
OUTPUT_RAVNICA_FILE = "path/to/output.json"
```

**Adjust difficulty classes** in `config.py`:
```python
CHALLENGE_RATINGS = {
    "3": {"Challenge": "3 (700 XP)", "Armor Class": 14, ...}
}
```

**Add new keywords** in `config.py`:
```python
KEYWORDS = {
    "Deathtouch": "<property-block>...</property-block>",
}
```

## Dependencies

- Python 3.8+
- json (stdlib)
- logging (stdlib)
- math (stdlib)
- fractions (stdlib)
- pathlib (stdlib)
- typing (stdlib)
- re (stdlib)

## Logging

The application uses Python's standard logging module. Adjust log level in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # For verbose output
```

## Contributing

The modular structure makes it easy to extend:
- Add new stat calculation methods to `stats_calculator.py`
- Create new converter classes for other file formats
- Add configuration options to `config.py`
- Implement new creature type logic in `creature_converter.py`

## Future Improvements

- [ ] Async file I/O for better performance on large datasets
- [ ] Configuration file support (YAML/JSON)
- [ ] Unit tests for each module
- [ ] CLI arguments for custom input/output paths
- [ ] Progress bar for long operations
- [ ] Database backend for creature lookups
- [ ] Web API for stats lookup
- [ ] Data validation and schema checking

## License

See original repository: https://github.com/themissenoone/mtgCreatures
