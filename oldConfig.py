"""Configuration and data definitions for MTG to D&D conversion."""

# D&D 5e Challenge Rating data
CHALLENGE_RATINGS = {
    "0": {"Challenge": "0 (10 XP)", "Armor Class": 10, "Hit Points": 10, "bonus": 1, "DC": 10},
    "1/8": {"Challenge": "1/8 (25 XP)", "Armor Class": 13, "Hit Points": 15, "bonus": 2, "DC": 13},
    "1/4": {"Challenge": "1/4 (50 XP)", "Armor Class": 13, "Hit Points": 20, "bonus": 2, "DC": 13},
    "1/2": {"Challenge": "1/2 (100 XP)", "Armor Class": 13, "Hit Points": 30, "bonus": 3, "DC": 13},
    "1": {"Challenge": "1 (200 XP)", "Armor Class": 13, "Hit Points": 40, "bonus": 3, "DC": 13},
    "2": {"Challenge": "2 (450 XP)", "Armor Class": 13, "Hit Points": 50, "bonus": 3, "DC": 13},
    "3": {"Challenge": "3 (700 XP)", "Armor Class": 14, "Hit Points": 65, "bonus": 4, "DC": 13},
    "4": {"Challenge": "4 (1100 XP)", "Armor Class": 14, "Hit Points": 80, "bonus": 4, "DC": 14},
    "5": {"Challenge": "5 (1800 XP)", "Armor Class": 15, "Hit Points": 95, "bonus": 4, "DC": 15},
    "6": {"Challenge": "6 (2300 XP)", "Armor Class": 15, "Hit Points": 110, "bonus": 4, "DC": 15},
    "7": {"Challenge": "7 (2900 XP)", "Armor Class": 15, "Hit Points": 130, "bonus": 5, "DC": 15},
    "8": {"Challenge": "8 (3900 XP)", "Armor Class": 16, "Hit Points": 150, "bonus": 5, "DC": 16},
    "9": {"Challenge": "9 (5000 XP)", "Armor Class": 16, "Hit Points": 170, "bonus": 5, "DC": 16},
    "10": {"Challenge": "10 (5900 XP)", "Armor Class": 17, "Hit Points": 200, "bonus": 5, "DC": 16},
    "11": {"Challenge": "11 (7200 XP)", "Armor Class": 17, "Hit Points": 220, "bonus": 5, "DC": 17},
    "12": {"Challenge": "12 (8400 XP)", "Armor Class": 17, "Hit Points": 240, "bonus": 6, "DC": 18},
    "13": {"Challenge": "13 (10000 XP)", "Armor Class": 18, "Hit Points": 260, "bonus": 6, "DC": 18},
    "14": {"Challenge": "14 (11500 XP)", "Armor Class": 18, "Hit Points": 280, "bonus": 6, "DC": 18},
    "15": {"Challenge": "15 (13000 XP)", "Armor Class": 18, "Hit Points": 300, "bonus": 6, "DC": 18},
    "16": {"Challenge": "16 (15000 XP)", "Armor Class": 18, "Hit Points": 320, "bonus": 6, "DC": 18},
    "17": {"Challenge": "17 (18000 XP)", "Armor Class": 19, "Hit Points": 330, "bonus": 6, "DC": 19},
    "18": {"Challenge": "18 (20000 XP)", "Armor Class": 19, "Hit Points": 350, "bonus": 6, "DC": 19},
    "19": {"Challenge": "19 (22000 XP)", "Armor Class": 19, "Hit Points": 370, "bonus": 7, "DC": 19},
    "20": {"Challenge": "20 (25000 XP)", "Armor Class": 19, "Hit Points": 400, "bonus": 7, "DC": 19},
    "21": {"Challenge": "21 (33000 XP)", "Armor Class": 20, "Hit Points": 450, "bonus": 7, "DC": 20},
    "22": {"Challenge": "22 (41000 XP)", "Armor Class": 20, "Hit Points": 500, "bonus": 7, "DC": 20},
    "23": {"Challenge": "23 (50000 XP)", "Armor Class": 20, "Hit Points": 550, "bonus": 8, "DC": 21},
    "24": {"Challenge": "24 (62000 XP)", "Armor Class": 21, "Hit Points": 600, "bonus": 8, "DC": 21},
    "25": {"Challenge": "25 (75000 XP)", "Armor Class": 21, "Hit Points": 650, "bonus": 8, "DC": 21},
    "26": {"Challenge": "26 (90000 XP)", "Armor Class": 21, "Hit Points": 700, "bonus": 8, "DC": 21},
    "27": {"Challenge": "27 (105000 XP)", "Armor Class": 22, "Hit Points": 800, "bonus": 8, "DC": 22},
    "28": {"Challenge": "28 (120000 XP)", "Armor Class": 22, "Hit Points": 900, "bonus": 9, "DC": 22},
    "29": {"Challenge": "29 (135000 XP)", "Armor Class": 22, "Hit Points": 1000, "bonus": 9, "DC": 22},
    "30": {"Challenge": "30 (155000 XP)", "Armor Class": 22, "Hit Points": 1100, "bonus": 9, "DC": 23},
}

# D&D 5e Ability Scores
ATTRIBUTES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

# Creature types
CREATURE_TYPES = [
    "Viashino", "Shaman", "Drake", "Vedalken", "Nephilim", "Advisor",
    "Mutant", "Leviathan", "Soldier", "Archon", "Bird", "Griffin",
    "Barbarian", "Wurm", "Archer", "Thrull", "Jellyfish", "Shade",
    "Shapeshifter", "Dinosaur", "Phoenix", "Slug", "Antelope", "Sheep",
    "Minion", "Fish", "Praetor", "Hellion", "Monk", "Pilot", "Lammasu",
    "Mercenary",
]

# MTG Color traits converted to D&D abilities
COLOR_TRAITS = {
    "azorius": "<property-block><h4>Azorius Authority.</h4><p>You have advantage on Intelligence (History) checks related to legal matters, and you can use your proficiency bonus instead of your Charisma modifier for any Persuasion checks made during legal negotiations or discussions.</p></property-block>",
    "dimir": "<property-block><h4>Infiltrator's Guise.</h4><p>You have a knack for slipping through the shadows and blending in with your surroundings. You have advantage on Dexterity (Stealth) checks made to hide or move silently.</p></property-block>",
    "rakdos": "<property-block><h4>Rakdos Fervor.</h4><p>You thrive in chaotic and frenetic environments. You have advantage on Constitution saving throws against exhaustion and resistance to effects that would cause you to become frightened or charmed.</p></property-block>",
    "golgari": "<property-block><h4>Natural Resilience.</h4><p>Your connection to the Golgari Swarm grants you an innate resilience to toxins and poisons. You have advantage on Constitution saving throws against poison and resistance to poison damage.</p></property-block>",
    "selesnya": "<property-block><h4>Harmony of the Conclave.</h4><p>Your connection to the Selesnya Conclave allows you to channel the unity and harmony of nature. You have advantage on Wisdom (Nature) checks and can use your proficiency bonus instead of your Wisdom modifier for any Animal Handling checks made to interact with natural creatures.</p></property-block>",
    "orzhov": "<property-block><h4>Business Acumen.</h4><p>Your affiliation with the Orzhov Syndicate grants you a keen understanding of financial matters. You have advantage on Intelligence (Investigation) checks related to financial transactions and can use your proficiency bonus instead of your Wisdom modifier for any Insight checks made during negotiations or dealings with monetary value.</p></property-block>",
    "izzet": "<property-block><h4>Innovator's Ingenuity.</h4><p>Your membership in the Izzet League fuels your innovative spirit. You have advantage on Intelligence (Arcana) checks related to experimental magic and can use your proficiency bonus instead of your Dexterity modifier for any Sleight of Hand checks made to manipulate or modify magical devices.</p></property-block>",
    "gruul": "<property-block><h4>Savage Instincts.</h4><p>Your connection to the Gruul Clans enhances your primal instincts. You have advantage on Wisdom (Survival) checks made to track or hunt creatures, and you gain proficiency in the Intimidation skill.</p></property-block>",
    "boros": "<property-block><h4>Military Precision.</h4><p>Your training with the Boros Legion instills in you a sense of military discipline and precision. You have advantage on Dexterity (Initiative) checks to determine the order of combat and can use your proficiency bonus instead of your Strength modifier for any Athletics checks made in combat situations.</p></property-block>",
    "simic": "<property-block><h4>Natural Adaptation.</h4><p>Your association with the Simic Combine allows you to tap into the natural world's adaptability. You have advantage on Constitution saving throws against diseases and poisons, and you can use your proficiency bonus instead of your Intelligence modifier for any Medicine checks made to treat natural creatures.</p></property-block>",
}

# MTG Keywords mapped to D&D abilities
KEYWORDS = {
    "Counter": "<property-block><h4>Counter a Spell.</h4><p>Whenever this effect triggers, the creature creates a 15 foot antimagic cube centered on a point it can see within 30 feet.</p></property-block>",
    "Deathtouch": "<property-block><h4>Deathtouch.</h4><p>At the beginning of this creature's second turn they coat their weapons and body in poison. All attacks the creature makes deal an extra 1d6 poison damage on hit.</p></property-block>",
    "Defender": "<property-block><h4>Defender.</h4><p>This creature cannot take the attack action normally on their turn. When attacked they may make an attack action targeting its attacker.</p></property-block>",
    "Flying": "<property-block><h4>Flying.</h4><p>Has a flying speed equal to its movement speed. If it hasn't attacked this round it does not provoke opportunity attacks.</p></property-block>",
    "Haste": "<property-block><h4>Haste.</h4><p>This creature has advantage on initiative rolls and advantage on each attack it makes in the first round of combat.</p></property-block>",
    "Hexproof": "<property-block><h4>Hexproof.</h4><p>This creature has advantage on saving throws against magical effects and resistance to magical damage.</p></property-block>",
    "Indestructible": "<property-block><h4>Indestructible.</h4><p>This creature has immunity to bludgeoning, piercing, or slashing damage from non-magical weapons.</p></property-block>",
    "Lifelink": "<property-block><h4>Lifelink.</h4><p>As a bonus action, this creature may invoke its life-draining properties. The next time it deals damage this turn, it gains that much life.</p></property-block>",
    "Menace": "<property-block><h4>Menace.</h4><p>At the beginning of its turn, as a bonus action if the creature has half HP or less, it lets out a menacing aura.</p></property-block>",
    "Reach": "<property-block><h4>Reach.</h4><p>+5 feet to melee range.</p></property-block>",
    "Trample": "<property-block><h4>Trample.</h4><p>As a bonus action, this creature may move up to its movement speed through creatures as if they weren't there.</p></property-block>",
    "Vigilance": "<property-block><h4>Vigilance.</h4><p>Whenever this creature makes a successful attack of opportunity, it regains the use of its reaction.</p></property-block>",
}

# Card rarity to power multiplier
RARITY_MULTIPLIERS = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "mythic": 5,
}

# File paths
INPUT_MONSTERS_FILE = "monsters.json"
INPUT_RAVNICA_FILE = "ravnicaCreatures.json"
OUTPUT_MONSTERS_FILE = "finalMonsters.json"
OUTPUT_RAVNICA_FILE = "final.json"
NEW_TYPES_LOG_FILE = "newTypes.txt"