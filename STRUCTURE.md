# Repository Structure Guide

This project is organized into the following directory structure:

## 📁 Project Layout

```
mtgCreatures/
├── README.md                          # Main project documentation
├── main.py                            # Entry point for the conversion pipeline
├── index.html                         # Main web interface
│
├── src/                               # Frontend source files
│   ├── js/                           # JavaScript files
│   │   ├── app.js                    # Main app entry point
│   │   ├── script.js                 # DOM manipulation
│   │   ├── encounters.js             # Encounter generator logic
│   │   ├── stat-block.js             # Stat block rendering
│   │   ├── abilities-block.js        # Ability rendering
│   │   ├── creature-heading.js       # Heading rendering
│   │   ├── property-block.js         # Property display
│   │   ├── property-line.js          # Individual properties
│   │   ├── tapered-rule.js           # Visual separator
│   │   ├── top-stats.js              # Top stat rendering
│   │   └── helpers/
│   │       └── create-custom-element.js   # Web component utilities
│   ├── templates/                    # HTML templates
│   │   ├── abilities-block.html
│   │   ├── creature-heading.html
│   │   ├── property-block.html
│   │   ├── property-line.html
│   │   ├── stat-block.html
│   │   ├── tapered-rule.html
│   │   └── top-stats.html
│   ├── styles/
│   │   └── style.css                 # Main stylesheet
│   ├── encounters.html               # Encounter generator interface
│   └── test-encounters.html          # Testing interface for encounters
│
├── backend/                           # Python backend processing
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # Conversion pipeline entry point
│   ├── config.py                     # Configuration and trait definitions
│   ├── creature_converter.py         # MTG → D&D conversion logic
│   ├── stats_calculator.py           # D&D stat calculations and scaling
│   ├── file_utils.py                 # File I/O utilities
│   ├── logs/
│   │   └── conversion.log            # Conversion pipeline logs
│   └── analysis/                     # Analysis and verification scripts
│       ├── __init__.py
│       ├── analyze_creatures.py      # Creature statistics
│       ├── analyze_trait_costs.py    # Trait cost analysis
│       ├── analyze_action_scaling.py # Action damage scaling analysis
│       ├── analyze_defensive_budgets.py  # AC/HP validation
│       ├── verify_action_scaling.py  # Action scaling verification
│       ├── verify_all_systems.py     # Complete system verification
│       ├── check_colors.py           # Guild color validation
│       ├── check_rat_fixed.py        # Specific creature validation
│       └── test-encounter-system.py  # Encounter system testing
│
├── data/                             # Data files
│   ├── source/                       # Input data
│   │   ├── monsters.json             # Base creature definitions
│   │   ├── ravnicaCreatures.json     # MTG Ravnica cards
│   │   └── ravnicaCreaturesTypes.json # Card type mappings
│   ├── output/                       # Processed output
│   │   ├── final.json                # Converted and balanced creatures
│   │   └── finalMonsters.json        # Base creature output
│   └── temp/                         # Temporary files
│       └── newTypes.txt              # Type discovery log
│
├── docs/                             # Documentation
│   ├── ACTION_SCALING.md             # Action damage scaling documentation
│   ├── COMPLETE_BALANCING_SYSTEM.md  # Full system overview
│   ├── DEFENSIVE_BUDGETING.md        # AC/HP budgeting details
│   ├── TRAIT_SYSTEM.md               # Trait cost system
│   ├── MOBILE_UI_IMPROVEMENTS.md     # UI changes
│   ├── SCALING_QUICK_REFERENCE.md    # Quick reference guide
│   ├── QUICKSTART.md                 # Getting started guide
│   ├── REFACTORING_GUIDE.md          # Code organization guide
│   ├── CHANGELOG.md                  # Version history
│   ├── SYSTEM_SUMMARY.md             # System overview
│   └── SUMMARY.md                    # Project summary
│
└── scripts/                          # Utility scripts (wrappers)
    ├── analyze_defensive_budgets.py
    ├── analyze_trait_costs.py
    └── verify_all_systems.py
```

## 🚀 Quick Start

### Running the Conversion Pipeline
```bash
# From project root, run the conversion pipeline
python main.py

# This will:
# 1. Read source data from data/source/
# 2. Convert MTG cards to D&D 5e creatures
# 3. Apply trait budgeting and balancing
# 4. Output results to data/output/
```

### Running Analysis Scripts
```bash
# From project root, run analysis scripts
python backend/analysis/analyze_defensive_budgets.py
python backend/analysis/verify_all_systems.py
python backend/analysis/analyze_trait_costs.py
```

### Opening the Web Interface
```bash
# Open index.html in your browser to view creatures
# Open src/encounters.html to test the encounter generator
```

## Data Flow

```
data/source/
├── monsters.json          Stage 1: Base processing
├── ravnicaCreatures.json
└── ravnicaCreaturesTypes.json
        ↓
  MonsterProcessor
  RavnicaCardConverter
        ↓
  Applied Systems:
  ├─ Trait Budgeting
  ├─ Defensive Budgeting (AC/HP)
  ├─ Action Scaling
  └─ CR Validation
        ↓
data/output/
├── final.json             (Main output: 920 creatures)
└── finalMonsters.json
```

## 🔧 Backend System Layers

### Layer 1: Trait System (`config.py`)
- 50+ D&D 5e-aligned keywords
- 10 Ravnica guilds as trait sources
- CR-based trait point budgets (1-16 points max)

### Layer 2: Defensive Budgeting (`stats_calculator.py`)
- AC ranges per CR (10-22 scale)
- HP ranges per CR (1-780 scale)
- Automatic validation and capping

### Layer 3: Action Scaling (`stats_calculator.py`)
- Damage dice scaling by CR tier
- Attack bonus adaptation
- Action complexity management

### Layer 4: CR Validation (`creature_converter.py`)
- Challenge Rating consistency checks
- Multi-layer compliance verification
- Creature power verification

## 📝 Key Configuration Files

### `backend/config.py`
Contains all trait definitions, costs, and game mechanics configuration.
- `TRAIT_BUDGETS`: CR → max trait points mapping
- `KEYWORD_BALANCE`: 50+ traits with costs and mechanics
- `COLOR_TRAIT_BALANCE`: 10 Ravnica guilds
- `CHALLENGE_RATINGS`: D&D CR definitions
- File paths (automatically resolve to data/ folders)

### `backend/stats_calculator.py`
Contains all mathematical calculations and scaling.
- `AC_BUDGETS`: AC ranges by CR
- `HP_BUDGETS`: HP ranges by CR
- Validation and scaling functions

## 📚 Documentation

All documentation is in the `docs/` folder:
- **COMPLETE_BALANCING_SYSTEM.md** - Start here for system overview
- **QUICKSTART.md** - Quick reference for get starting
- **ACTION_SCALING.md** - Damage scaling details
- **DEFENSIVE_BUDGETING.md** - AC/HP system details
- **TRAIT_SYSTEM.md** - Trait costs and mechanics
- **SCALING_QUICK_REFERENCE.md** - Quick lookup reference

## 🧪 Testing & Verification

Run verification scripts from project root:

```bash
# Complete system verification
python backend/analysis/verify_all_systems.py

# Defensive budgeting analysis
python backend/analysis/analyze_defensive_budgets.py

# Trait cost analysis
python backend/analysis/analyze_trait_costs.py

# Specific creature checks
python backend/analysis/check_rat_fixed.py
```

## 📡 Web Interface Files

- **index.html** - Main creature browser
- **src/encounters.html** - Encounter generator
- **src/styles/style.css** - Responsive design
- **src/js/*.js** - Frontend logic

The web interface loads creatures from `data/output/final.json`.

## 🔄 Adding New Features

1. **New Trait**: Add to `KEYWORD_BALANCE` in `config.py`
2. **New Analysis**: Create script in `backend/analysis/`
3. **UI Changes**: Modify files in `src/`
4. **Balance Adjustments**: Update `stats_calculator.py` and `config.py`

## 📋 Development Workflow

1. Modify source data in `data/source/`
2. Update conversion logic in `backend/creature_converter.py`
3. Adjust balance parameters in `backend/config.py` and `backend/stats_calculator.py`
4. Run `python main.py` to rebuild
5. Run analysis scripts to verify
6. Check web interface or generated JSON

---

**Last Updated**: March 2026
**Status**: Production Ready (4-layer balancing system complete)
