"""Configuration and data definitions for MTG to D&D conversion.
Este arquivo mantém as estruturas anteriores (CHALLENGE_RATINGS, ATTRIBUTES, etc.)
e adiciona BALANCEAMENTO NUMÉRICO para cada trait/keyword/mecânica de Ravnica,
além de incluir traits específicos dos blocos Ravnica (Original, RTR, Guilds).

TRAIT COST SYSTEM (D&D 5e aligned):
- Cada trait tem um "cost" em pontos de complexidade (0-5).
- CR 0-2: máximo 2 pontos (tipicamente 1 trait simples ou nenhum).
- CR 3-5: máximo 4 pontos (2-3 traits pequenos/1 trait médio).
- CR 6-8: máximo 5 pontos (2-3 traits médios).
- CR 9+: máximo 7 pontos (múltiplos traits potentes).
- Traits reduzidos (lite versions em parenteses) custam metade do cost.

Design notes:
- Traits agora focam em ações/reações 5e (Legendary Actions, Reactions, etc).
- Cada keyword/trait tem:
    * uma representação HTML (compatível com statblock5e) em KEYWORDS / COLOR_TRAITS
    * custo (cost); impacts na seleção e frequência de aplicação.
    * dicionário numérico correspondente em KEYWORD_BALANCE / COLOR_TRAIT_BALANCE
      que contém ajustes de CR e modificadores mecânicos (dpr, hp, saves).
"""

# ==========================================================
# D&D 5e Challenge Rating data (unchanged)
# ==========================================================

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


ATTRIBUTES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

CREATURE_TYPES = [
    "Viashino", "Shaman", "Drake", "Vedalken", "Nephilim", "Advisor",
    "Mutant", "Leviathan", "Soldier", "Archon", "Bird", "Griffin",
    "Barbarian", "Wurm", "Archer", "Thrull", "Jellyfish", "Shade",
    "Shapeshifter", "Dinosaur", "Phoenix", "Slug", "Antelope", "Sheep",
    "Minion", "Fish", "Praetor", "Hellion", "Monk", "Pilot", "Lammasu",
    "Mercenary",
]

# ==========================================================
# COLOR TRAITS (HTML for statblock) - mantemos HTML
# ==========================================================
# (melhorados anteriormente; aqui mantemos as strings para compatibilidade)
COLOR_TRAITS = {
    "azorius": "<property-block><h4>Azorius Authority.</h4><p>Once per combat, the creature can cast <em>Hold Person</em> (DC based on CR) without components. It has advantage on Intelligence (History) and Investigation checks related to law and governance.</p></property-block>",

    "dimir": "<property-block><h4>Dimir Operative.</h4><p>The creature has advantage on Dexterity (Stealth). During the first round of combat, attacks made against surprised creatures are automatic critical hits.</p></property-block>",

    "rakdos": "<property-block><h4>Rakdos Fervor.</h4><p>When reduced below half its hit points, the creature gains advantage on attack rolls and adds 1d8 fire damage to all attacks until the end of its next turn.</p></property-block>",

    "golgari": "<property-block><h4>Golgari Resilience.</h4><p>The creature has resistance to poison and necrotic damage. When reduced to 0 HP, it can make a Constitution saving throw (DC 10 + damage taken) to instead drop to 1 HP.</p></property-block>",

    "selesnya": "<property-block><h4>Conclave Unity.</h4><p>All allied creatures within 10 feet gain +1 AC. The creature can cast <em>Entangle</em> once per combat.</p></property-block>",

    "orzhov": "<property-block><h4>Debt Collector.</h4><p>Whenever this creature deals damage, the target must succeed on a Wisdom saving throw or have disadvantage on its next attack roll.</p></property-block>",

    "izzet": "<property-block><h4>Arcane Overload.</h4><p>Once per combat, when the creature casts a spell or deals elemental damage, it may maximize one damage die.</p></property-block>",

    "gruul": "<property-block><h4>Clan Rampage.</h4><p>If the creature moves at least 20 feet straight toward a target and hits it with a melee attack, the attack deals an extra 2d8 damage.</p></property-block>",

    "boros": "<property-block><h4>Legion Tactics.</h4><p>The creature adds its proficiency bonus to initiative. If an ally is within 5 feet of the target, it deals an extra 1d6 damage.</p></property-block>",

    "simic": "<property-block><h4>Adaptive Evolution.</h4><p>At the start of each of its turns, the creature may choose to gain resistance to one damage type until the start of its next turn.</p></property-block>",
}

# ==========================================================
# NUMERIC BALANCE: per-color trait (how afeta CR / stats)
# ==========================================================
# Cada cor/guild trait tem ajustes numéricos para ajudar o StatBlockCalculator
# a ajustar CR ou valores defensivos/ofensivos automaticamente.
#
# Campos:
#   - cr_offense: ajuste aproximado de CR no lado ofensivo (float)
#   - cr_defense: ajuste aproximado de CR no lado defensivo (float)
#   - dpr_bonus: valor aproximado de DPS (DPR) extra por rodada que a trait confere
#   - hp_multiplier: multiplicador direto de HP (ex: 1.2 = +20% HP)
#   - notes: orientações de aplicação
COLOR_TRAIT_BALANCE = {

    "azorius": {"cost": 2, "cr_offense": 0.2, "cr_defense": 0.6, "dpr_bonus": 0.0, "hp_multiplier": 1.00,
                "mechanism": "Save Throw + Control",
                "notes": "Controle tático; usa saves (Hold Person). Favor usar para criaturas com capacidade inteligente de combate. Legendary Action + Recharge."},

    "dimir": {"cost": 2, "cr_offense": 0.6, "cr_defense": 0.3, "dpr_bonus": 2.5, "hp_multiplier": 1.00,
              "mechanism": "Assassinate + Stealth",
              "notes": "Assassino/stealth — aumenta DPR inicial em surprise rounds. Advantage on Stealth, critical hits vs surprised creatures. Reaction-based."},

    "rakdos": {"cost": 2, "cr_offense": 0.8, "cr_defense": -0.1, "dpr_bonus": 3.0, "hp_multiplier": 1.00,
               "mechanism": "Fervor + High Damage",
               "notes": "Alto dano em explosão; mais ofensivo que defensivo. When bloodied, gain advantage on attacks. Extra d8 fire damage."},

    "golgari": {"cost": 2, "cr_offense": 0.3, "cr_defense": 1.0, "dpr_bonus": 0.5, "hp_multiplier": 1.20,
                "mechanism": "Regeneration + Evasion",
                "notes": "Recursão/resistência; aumenta efetivamente HP e durabilidade. Resistance to necrotic/poison. Regains 1d4 HP at end of turn."},

    "selesnya": {"cost": 2, "cr_offense": 0.2, "cr_defense": 0.6, "dpr_bonus": 0.5, "hp_multiplier": 1.05,
                 "mechanism": "Aura + Team Buff",
                 "notes": "Buff de aliados; utilitário defensivo em grupo. All allies within 10ft gain +1 AC. Aura effect, not ability-based."},

    "orzhov": {"cost": 2, "cr_offense": 0.3, "cr_defense": 0.4, "dpr_bonus": 0.8, "hp_multiplier": 1.00,
               "mechanism": "Drain + Debuff",
               "notes": "Drain/controle; penaliza inimigos em retribuição. When attacks hit, target has disadvantage on next attack. Reaction-based drain 1d4 HP."},

    "izzet": {"cost": 2, "cr_offense": 0.7, "cr_defense": 0.0, "dpr_bonus": 2.0, "hp_multiplier": 1.00,
              "mechanism": "Spell-like + High Damage",
              "notes": "Explosões de dano mágico; maximização ocasional aumenta DPR efetivo. Spell-like ability (recharge per day). Can max one damage die per spell."},

    "gruul": {"cost": 2, "cr_offense": 0.9, "cr_defense": 0.1, "dpr_bonus": 4.0, "hp_multiplier": 1.00,
             "mechanism": "Mobile + Extra Damage",
             "notes": "High DPR quando se move e ataca; ruim sem mobilidade. If moves 20+ ft and hits, adds 2d8 damage. Disadvantage when immobilized."},

    "boros": {"cost": 2, "cr_offense": 0.5, "cr_defense": 0.4, "dpr_bonus": 1.5, "hp_multiplier": 1.00,
              "mechanism": "Team Attack + Tactics",
              "notes": "Sinergia em grupo; vantagem tática. Adds proficiency to initiative. Extra 1d6 damage if ally within 5ft of target. Bonus Action ability."},

    "simic": {"cost": 2, "cr_offense": 0.4, "cr_defense": 0.6, "dpr_bonus": 0.5, "hp_multiplier": 1.10,
              "mechanism": "Adaptive + Resistances",
              "notes": "Adaptabilidade -> aumenta defesa e utilidade. At start of turn, choose 1 damage resistance (resets each turn). HP multiplier reflects hardiness."},
}


# ==========================================================
# KEYWORDS (D&D 5e mechanics for statblock display)
# ==========================================================
# MTG keywords converted to authentic D&D 5e mechanics
KEYWORDS = {

    # Core MTG → D&D 5e conversions
    "Flying": "<property-block><h4>Flight.</h4><p>The creature has a flying speed equal to its walking speed. Creatures on the ground have disadvantage on melee attack rolls against this creature.</p></property-block>",

    "Haste": "<property-block><h4>Pent-Up Energy.</h4><p>The creature gains a +2 bonus to initiative rolls. On its first turn of combat, it can use its bonus action to take the Attack action.</p></property-block>",

    "Vigilance": "<property-block><h4>Combat Readiness.</h4><p>When this creature makes a melee attack, it doesn't provoke opportunity attacks from the target and its defensive reaction isn't expended.</p></property-block>",

    "Trample": "<property-block><h4>Trampling Charge.</h4><p>When the creature moves through a hostile creature's space and succeeds on a melee attack roll, it can move through that creature's space as if the space were difficult terrain. If the creature ends its movement in an occupied space, that creature is knocked prone.</p></property-block>",

    "Lifelink": "<property-block><h4>Life Drain.</h4><p>Whenever this creature deals damage to a creature, the creature that dealt the damage regains hit points equal to half the damage dealt (minimum 1).</p></property-block>",

    "Deathtouch": "<property-block><h4>Necrotic Aura.</h4><p>Any creature hit by this creature's attack must succeed on a Constitution saving throw (DC = 8 + the creature's proficiency bonus + its Strength or Dexterity modifier) or take an additional 1d6 necrotic damage and be vulnerable to necrotic damage until the end of its next turn.</p></property-block>",

    "Hexproof": "<property-block><h4>Magic Resistance.</h4><p>The creature has advantage on saving throws against spells and magical effects. Spells and magical effects cannot target this creature unless it allows it (it can allow beneficial effects).</p></property-block>",

    "Indestructible": "<property-block><h4>Undying.</h4><p>The creature has resistance to all damage. When reduced to 0 hit points, it can make a Constitution saving throw (DC 10 + damage taken) to instead drop to 1 hit point instead.</p></property-block>",

    "Reach": "<property-block><h4>Long Reach.</h4><p>This creature's melee attacks have a reach of 10 feet, instead of 5 feet.</p></property-block>",

    "Menace": "<property-block><h4>Menacing Presence.</h4><p>A creature must have advantage on attack rolls to hit this creature, unless at least two other creatures are within 5 feet of this creature. This creature also has advantage on attack rolls against creatures it's flanking.</p></property-block>",

    "First Strike": "<property-block><h4>Reactive Strike.</h4><p>The creature has a +3 bonus to initiative. During the first round of combat, this creature can take an additional reaction.</p></property-block>",

    "Double Strike": "<property-block><h4>Rapid Strike.</h4><p>When the creature takes the Attack action on its turn, it can make one additional attack using the same action.</p></property-block>",

    "Flash": "<property-block><h4>Sudden Appearance.</h4><p>This creature can use its reaction when initiative is rolled to enter combat immediately, taking its turn before creatures with lower initiative.</p></property-block>",

    "Defender": "<property-block><h4>Guardian's Stance.</h4><p>This creature cannot take the Attack action on its turn. Instead, it can make a melee attack with disadvantage as a reaction when a hostile creature enters its reach.</p></property-block>",

    # Ravnica-specific mechanics (D&D 5e aligned)
    "Forecast": "<property-block><h4>Predictive Analysis.</h4><p>At the start of each of its turns, this creature can use its bonus action to prepare a tactical response. Until the start of its next turn, the creature gains advantage on initiative or adding +2 to its next attack roll.</p></property-block>",

    "Radiance": "<property-block><h4>Radiating Effect.</h4><p>When this creature uses an ability that affects a target, up to three other creatures of the same creature type within 30 feet must make a Wisdom saving throw (same DC) or be affected by half the effect (rounded down).</p></property-block>",

    "Transmute": "<property-block><h4>Adaptive Tactics.</h4><p>As an action, this creature can swap one of its ability scores (minimum 3, maximum 18) for another prepared ability within 24 hours of preparation (equivalent to a long rest). It can use this trait only once per long rest.</p></property-block>",

    "Dredge": "<property-block><h4>Resurrection Recovery.</h4><p>When this creature is reduced to 0 hit points, it can make a Constitution saving throw (DC 10 + damage taken). On a success, it regains 1d6 hit points instead and must complete a long rest before using this trait again.</p></property-block>",

    "Bloodthirst": "<property-block><h4>Battle Fury.</h4><p>When this creature enters combat and an enemy has already taken damage this turn, this creature gains +2 to its attack rolls and deals an extra 1d6 damage with weapon attacks until the end of its next turn.</p></property-block>",

    "Replicate": "<property-block><h4>Mirrored Action.</h4><p>When this creature uses an ability that affects one target, it can pay an additional cost (expending a use of another ability) to target up to two additional creatures within 30 feet with the same effect.</p></property-block>",

    "Haunt": "<property-block><h4>Lingering Spirit.</h4><p>When this creature would be reduced to 0 hit points by a creature it can see, it can instead become invisible and intangible until the end of its next turn, moving up to half its speed. The triggering creature must make a Wisdom saving throw (DC = 8 + Proficiency + Charisma mod) or be frightened until the end of its next turn.</p></property-block>",

    "Hellbent": "<property-block><h4>Desperate Power.</h4><p>When this creature has no bonus actions remaining on its turn, it gains +1 to its attack rolls and damage rolls until the end of its turn.</p></property-block>",

    "Convoke": "<property-block><h4>Communal Power.</h4><p>This creature's allies within 10 feet can use their reaction to grant this creature advantage on an ability check or attack roll it's making. A creature can use this reaction only once per turn.</p></property-block>",

    "Graft": "<property-block><h4>Adaptive Growth.</h4><p>This creature enters with 2 growth counters. When another allied creature enters the battlefield within 5 feet, this creature can move one growth counter to that creature, increasing its attack and damage rolls by +1 until the counter is removed.</p></property-block>",

    "Detain": "<property-block><h4>Binding Hold.</h4><p>As an action, this creature can target one creature it can see within 30 feet. The target must make a Strength saving throw (DC = 8 + Proficiency + Strength mod). On a failure, the target is restrained until the start of this creature's next turn. If the target is restrained at the start of its turn, it can repeat the save.</p></property-block>",

    "Battalion": "<property-block><h4>Coordinated Strike.</h4><p>When this creature attacks with at least two other allies within 5 feet of the target, this creature has advantage on the attack roll and deals an extra 1d6 damage on a hit.</p></property-block>",

    "Cipher": "<property-block><h4>Spell Cipher.</h4><p>When this creature deals melee damage to a creature, it can trigger one prepared spell-like ability (recharge 5–6). The ability is cast on the target without expending a spell slot.</p></property-block>",

    "Scavenge": "<property-block><h4>Carrion Recovery.</h4><p>As an action, this creature can gain temporary hit points equal to 1d6 + its Constitution modifier if a creature has died within 10 feet of it since its last turn. It can gain temporary hit points this way only once per day.</p></property-block>",

    "Bloodrush": "<property-block><h4>Frenzied Strike.</h4><p>As a reaction when a nearby creature attacks, this creature can make a melee attack roll with advantage against that creature. If the attack hits, the attacking creature has disadvantage on its attack roll.</p></property-block>",

    "Overload": "<property-block><h4>Cascade Effect.</h4><p>When this creature uses an ability that targets one creature, it can pay double the resource cost to target all creatures in a 20-foot radius instead. Affected creatures make a Dexterity saving throw (same DC) and take half damage on a success.</p></property-block>",

    "Extort": "<property-block><h4>Profane Drain.</h4><p>Whenever this creature deals damage with an ability, each creature within 10 feet of it must make a Wisdom saving throw (DC = 8 + Proficiency + Charisma mod) or take 1d4 psychic damage. This creature regains hit points equal to the total damage dealt.</p></property-block>",

    "Unleash": "<property-block><h4>Primal Fury.</h4><p>This creature can enter with a fury counter. While it has this counter, this creature cannot use reactions and its movement speed is increased by 10 feet, and it has advantage on Strength checks and saving throws. The counter persists until the end of combat.</p></property-block>",

    "Populate": "<property-block><h4>Conjured Ally.</h4><p>As a bonus action, this creature can create a duplicate of itself with half its hit points (rounded down) within 5 feet of it. The duplicate acts immediately after this creature in initiative and obeys this creature's mental commands. The duplicate lasts until the end of the encounter.</p></property-block>",

    "Evolve": "<property-block><h4>Adaptive Evolution.</h4><p>Whenever an allied creature with higher hit points than this creature enters within 10 feet of it, this creature gains a growth counter. When this creature gains 3 growth counters, it regains 1d8 hit points and loses all counters.</p></property-block>",

    "Addendum": "<property-block><h4>Tactical Amendment.</h4><p>If this creature uses an ability during its main action phase (before declaring an action), it gains advantage on the next ability check or save it makes before the end of its turn.</p></property-block>",

    "Mentor": "<property-block><h4>Tactical Guidance.</h4><p>When this creature hits with a melee attack, one allied creature within 5 feet gains a +2 bonus to its next attack roll before the end of this creature's next turn.</p></property-block>",

    "Surveil": "<property-block><h4>Tactical Assessment.</h4><p>As a bonus action, this creature can look at the next 3 creatures to act in initiative order within 60 feet. You can rearrange the order in which they will act (this affects initiative for this encounter only).</p></property-block>",

    "Undergrowth": "<property-block><h4>Graveyard Empowerment.</h4><p>For each allied dead or unconscious creature within 30 feet, this creature gains +1 to its attack rolls and damage rolls (maximum +5). When an unconscious creature regains consciousness, this bonus decreases by 1.</p></property-block>",

    "Riot": "<property-block><h4>Frenzied Entry.</h4><p>When this creature enters combat, it can choose one: gain a +2 bonus to attack rolls until the end of its next turn, or gain an additional reaction until the end of its next turn.</p></property-block>",

    "Jump-start": "<property-block><h4>Resurrection.</h4><p>When this creature would be reduced to 0 hit points, it can use its reaction to regain 1d8 + Constitution modifier hit points instead. It must complete a short rest before using this trait again.</p></property-block>",

    "Afterlife": "<property-block><h4>Spectral Echo.</h4><p>When this creature is reduced to 0 hit points, 1d4 spectral servants (1 HP, flying) appear in unoccupied spaces within 5 feet of it. They act immediately after this creature in initiative and obey its commands.</p></property-block>",

    "Spectacle": "<property-block><h4>Crowd Momentum.</h4><p>You can use this creature's ability for half the normal cost if an enemy within 30 feet has taken damage since the start of this creature's last turn.</p></property-block>",

    "Adapt": "<property-block><h4>Reactive Adaptation.</h4><p>As a bonus action on its turn, this creature can gain a mutations counter. When this creature gains 3 mutations counters, it gains advantage on all attack rolls and saving throws until the end of its next turn, then loses all counters.</p></property-block>",
}

# ==========================================================
# NUMERIC BALANCE: per-keyword (ajustes de CR e efeitos numéricos)
# ==========================================================
# Estrutura:
#   KEY: {
#       "cr_offense": float,     # ajuste aproximado de CR no lado ofensivo
#       "cr_defense": float,     # ajuste aproximado de CR no lado defensivo
#       "dpr_bonus": float,      # aumento aproximado de DPR por rodada (média)
#       "hp_delta": int,         # incremento de HP plano (use com CHALLENGE_RATINGS)
#       "save_dc_delta": int,    # delta a adicionar à DC padrão (8 + prof) quando aplicável
#       "notes": str
#   }
#
# Observação: aplicadores/convertors devem combinar múltiplos traits somando estes valores
# e arredondar o CR final conforme a tabela CHALLENGE_RATINGS.
# ==========================================================
# NUMERIC BALANCE: per-keyword (ajustes de CR e efeitos numéricos)
# ==========================================================
# Estrutura UPDATED with "cost" field:
#   KEY: {
#       "cost": int,             # trait complexity cost (1-5). Respects TRAIT_BUDGETS.
#       "cr_offense": float,     # ajuste aproximado de CR no lado ofensivo
#       "cr_defense": float,     # ajuste aproximado de CR no lado defensivo
#       "dpr_bonus": float,      # aumento aproximado de DPR por rodada (média)
#       "hp_delta": int,         # incremento de HP plano
#       "save_dc_delta": int,    # delta a adicionar à DC padrão
#       "mechanism": str,        # D&D 5e mechanism (Legendary Action, Reaction, Resistances, etc.)
#       "notes": str
#   }
#
# d&b 5e Mechanisms:
#  - Legendary Action: creature acts out of turn / extra action
#  - Reaction: immediate response to trigger
#  - Resistances: damage type resistances/immunities
#  - Saving Throw: adds save DC or advantage/disadvantage
#  - Evasion: halve or negate effects
#  - Regeneration: healing/recovery per turn
#  - Aura/Buff: affects nearby allies
#  - Recharge: spell/ability usable on recharge (short/long rest, per day, etc)

KEYWORD_BALANCE = {

    # Core - D&D 5e aligned with costs
    "Flying":        {"cost": 1, "cr_offense": 0.10, "cr_defense": 0.25, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Movement",
                      "notes": "Mobilidade defensiva; dificulta ataques corpo-a-corpo sem voo. Use Fly Speed = Walk Speed."},

    "Haste":         {"cost": 2, "cr_offense": 0.75, "cr_defense": -0.10, "dpr_bonus": 4.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Legendary Action",
                      "notes": "Ação adicional na primeira rodada ou por turn (limited). Usar como Legendary Action (costs 1 action) se CR >= 5."},

    "Vigilance":     {"cost": 1, "cr_offense": 0.10, "cr_defense": 0.25, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Reaction",
                      "notes": "Mantém reação e reduz vulnerabilidade ao atacar. Implementar como 'can use reaction and still attack'."},

    "Trample":       {"cost": 2, "cr_offense": 0.50, "cr_defense": 0.0, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Melee Action",
                      "notes": "Transfere dano excessivo contra múltiplos inimigos: aumenta DPR contra grupos. DC DEX save ou é derrubado."},

    "Lifelink":      {"cost": 2, "cr_offense": 0.10, "cr_defense": 0.75, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Regeneration",
                      "notes": "Regeneração via dano cauado; aumenta durabilidade. Heal = 50% damage dealt. Add +10 HP to reflect average healing per turn."},

    "Deathtouch":    {"cost": 3, "cr_offense": 2.00, "cr_defense": 0.0, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 2,
                      "mechanism": "Save Throw (CON)",
                      "notes": "Alvo ferido deve fazer save ou toma dano duplicado. DC = 8 + Proficiency + DEX/STR mod. Major offense boost!"},

    "Hexproof":      {"cost": 3, "cr_offense": 0.0, "cr_defense": 1.50, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Resistances+Evasion",
                      "notes": "Proteção contra direcionamento mágico: immunity to spells/effects unless choose. Forte aumento defensivo."},

    "Indestructible": {"cost": 4, "cr_offense": 0.0, "cr_defense": 3.00, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                       "mechanism": "Regeneration+Immunity",
                       "notes": "Não pode ser reduzido abaixo de 1 HP por dano + immunity to non-magical B/P/S. Impacto MUITO alto na resistência."},

    "Reach":         {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.0, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Melee",
                      "notes": "Aumenta alcance de ataque (10 ft vs 5 ft padrão). Facilita controlar espaço."},

    "Menace":        {"cost": 2, "cr_offense": 0.40, "cr_defense": 0.35, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Movement Restriction",
                      "notes": "Dificulta bloquear sem múltiplos atacantes: apply disadvantage to escapes/grapples unless enemy has 2+ allies adjacent."},

    "First Strike":  {"cost": 2, "cr_offense": 0.50, "cr_defense": 0.0, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Initiative/Action Order",
                      "notes": "Ataca antes em primeiro round: vantagem em matar alvos frágeis. +2 to Initiative for first round only."},

    "Double Strike": {"cost": 3, "cr_offense": 1.50, "cr_defense": 0.0, "dpr_bonus": 6.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Legendary Action",
                      "notes": "Ataque adicional em cada rodada; grande aumento de DPR. Use como Extra Action (costs 2 Legendary Actions if applicable)."},

    "Flash":         {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.15, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Reaction",
                      "notes": "Capacidade de entrar fora de hora na combat: can enter combat as a reaction when initiative rolls."},

    "Defender":      {"cost": 1, "cr_offense": -0.50, "cr_defense": 0.25, "dpr_bonus": -1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Reaction",
                      "notes": "Não pode atacar normalmente; papel de tanque/segurador. Can only attack as reaction when creature enters reach."},

    # Ravnica-specific / blocks - D&D 5e aligned with costs
    "Forecast":      {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Reaction",
                      "notes": "Pequeno efeito ativado no início do turno; utilitário contínuo. Use como recharge ability (recharge 5-6 per turn)."},

    "Radiance":      {"cost": 3, "cr_offense": 1.00, "cr_defense": 0.0, "dpr_bonus": 3.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Area Effect (Aura)",
                      "notes": "Efeito que se espalha — transforma alvo único em múltiplos alvos (perto com cores compatíveis). Usar como Aura (15-30ft)."},

    "Transmute":     {"cost": 1, "cr_offense": 0.20, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Bonus Action",
                      "notes": "Troca de efeitos (utility); pouco impacto direto no CR. Use como Long Rest recharge ability."},

    "Dredge":        {"cost": 2, "cr_offense": 0.10, "cr_defense": 1.00, "dpr_bonus": 0.5, "hp_delta": 10, "save_dc_delta": 0,
                      "mechanism": "Regeneration+Recharge",
                      "notes": "Recursão de habilidades: aumenta resiliência. Add HP pool and recharge ability from graveyard once per Long Rest."},

    "Bloodthirst":   {"cost": 2, "cr_offense": 0.50, "cr_defense": 0.0, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Conditional Bonus",
                      "notes": "Entra com bônus se oponente foi ferido — situacional. +2 to attack rolls and +1d6 damage if enemy took damage this turn."},

    "Replicate":     {"cost": 3, "cr_offense": 1.00, "cr_defense": 0.0, "dpr_bonus": 3.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Area Effect + Recharge",
                      "notes": "Copiar um efeito aumenta DPR efetivo; cada cópia custa ação. Use como recharge spell-like ability."},

    "Haunt":         {"cost": 2, "cr_offense": 0.60, "cr_defense": 0.40, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 1,
                      "mechanism": "Delayed Triggered Ability",
                      "notes": "Efeito retardado/recorrente — aumenta ofensa e resistência. Implementar como 'if haunted creature dies, trigger effect'."},

    "Hellbent":      {"cost": 2, "cr_offense": 0.50, "cr_defense": -0.25, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Conditional Bonus",
                      "notes": "Bonus forte com estômago vazio (condicional). +1 to attack rolls and +1d6 damage while no unused abilities remain."},

    "Convoke":       {"cost": 1, "cr_offense": 0.30, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Team Action",
                      "notes": "Habilidade de reduzir custos com aliados — utilitária. Allied creatures can expend minor resource to reduce cost."},

    "Graft":         {"cost": 1, "cr_offense": 0.40, "cr_defense": 0.40, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Buff/Buff Transfer",
                      "notes": "Contadores que podem ser redistribuídos; aumenta durabilidade e sinergia. Gain +1/+1 counter on entry; can move to allies."},

    "Detain":        {"cost": 2, "cr_offense": 1.00, "cr_defense": 0.50, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 2,
                      "mechanism": "Save Throw (WIS) + Restrained",
                      "notes": "Bloqueio de permanentes: forte controle. Target cannot use activated abilities, attack or block until next turn. Save allowed (DC per CR)."},

    "Battalion":     {"cost": 2, "cr_offense": 0.60, "cr_defense": 0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Team Attack",
                      "notes": "Dispara com ataque em grupo (3+ atacantes) — sinergia. +2d6 damage if attacking with 2+ ally creatures."},

    "Cipher":        {"cost": 3, "cr_offense": 1.50, "cr_defense": 0.0, "dpr_bonus": 5.0, "hp_delta": 0, "save_dc_delta": 1,
                      "mechanism": "Spell-like + Recharge",
                      "notes": "Repetição de feitiços ao causar dano — potencial ofensivo elevado. When hit, can cast encoded spell once (recharge per day)."},

    "Scavenge":      {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.60, "dpr_bonus": 0.5, "hp_delta": 5, "save_dc_delta": 0,
                      "mechanism": "Bonus Action+Buff",
                      "notes": "Exilar do cemitério para buff; tanto utilitário quanto defensivo. As action, exile 1 spent ability to gain +2 AC until end of turn."},

    "Bloodrush":     {"cost": 1, "cr_offense": 0.45, "cr_defense": -0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Reaction + Buff",
                      "notes": "Discard-to-buff; bom para combos. As reaction, give nearby ally +2 to attack and +1d6 damage until end of turn."},

    "Overload":      {"cost": 3, "cr_offense": 1.50, "cr_defense": -0.25, "dpr_bonus": 4.0, "hp_delta": 0, "save_dc_delta": 1,
                      "mechanism": "Area Effect (AoE Save)",
                      "notes": "Transforma alvo em AoE; muito poderoso em multi-alvo. Cast as AoE at +cost; all targets in 20ft radius make save or take half damage."},

    "Extort":        {"cost": 1, "cr_offense": 0.20, "cr_defense": 0.20, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Life Drain (Reaction)",
                      "notes": "Pequeno drain ao conjurar; acumula com múltiplos casts. When creature casts spell, drain 1d4 HP from neaby enemy and gain it."},

    "Unleash":       {"cost": 1, "cr_offense": 0.50, "cr_defense": -0.50, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Conditional Buff",
                      "notes": "+1/+1 ao entrar; não pode bloquear se tem marcador — trade-off ofensa/defesa. Gain +1 damage; cannot be targeted by protective effects."},

    "Populate":      {"cost": 2, "cr_offense": 0.50, "cr_defense": 0.40, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Summon + Team",
                      "notes": "Cria tokens — aumenta presença em campo. As bonus action, create 1 token copy of an ally creature (CR must allow)."},

    "Evolve":        {"cost": 1, "cr_offense": 0.45, "cr_defense": 0.45, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Scaling (Buff)",
                      "notes": "Escala com entrada de criiaturas maiores; bom em jogos longos. Whenever powerful ally enters, gain +1/+1 counter (max 3)."},

    "Addendum":      {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Conditional Bonus",
                      "notes": "Bônus se usado na main phase; pequena vantagem estratégica. If used before end of main phase, gain +2 to next attack."},

    "Mentor":        {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Team Buff",
                      "notes": "Coloca +1/+1 em aliados menores; melhora ataques. When attacking, give weaker ally +1 to attack rolls until end of turn."},

    "Surveil":       {"cost": 1, "cr_offense": 0.15, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Bonus Action (Utility)",
                      "notes": "Manipulação de topo de deck/efeitos futuros — utilitário. As bonus action, look at next 3 ability/actions and choose order."},

    "Undergrowth":   {"cost": 2, "cr_offense": 0.50, "cr_defense": 0.50, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Scaling (Dynamic)",
                      "notes": "Escala fortemente com número de cards de criatura no cemitério; escalável. Gain +1 to damage rolls per 3 spent abilities."},

    "Riot":          {"cost": 1, "cr_offense": 0.50, "cr_defense": 0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Choice Buff",
                      "notes": "Escolha entre +1/+1 ou haste — útil e simples. On entry, choose: +1 damage rolls OR take additional action this turn."},

    "Jump-start":    {"cost": 1, "cr_offense": 0.40, "cr_defense": 0.0, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Recharge (Graveyard)",
                      "notes": "Permite reusar feitiços do cemitério com custo; aumenta DPR em jogadas longas. Can reuse spent ability from graveyard (recharge per day)."},

    "Afterlife":     {"cost": 2, "cr_offense": 0.35, "cr_defense": 0.60, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Summon (On Death)",
                      "notes": "Spawn de tokens ao morrer — acrescenta resistência. When reduced to 0 HP, create 2d4 familiar spirit tokens (1 HP, flying)."},

    "Spectacle":     {"cost": 1, "cr_offense": 0.40, "cr_defense": 0.0, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Conditional Discount",
                      "notes": "Custo alternativo se oponente perdeu vida — situacionalmente poderoso. If enemy took damage this turn, ability costs 50% less."},

    "Adapt":         {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.25, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Bonus Action (Buff)",
                      "notes": "Pagamento por counters; pequeno buff por recurso. As bonus action, gain +1/+1 counter (once, then can't repeat)."},

    "Flash":         {"cost": 1, "cr_offense": 0.25, "cr_defense": 0.15, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Movement (Initiative)",
                      "notes": "Capacidade de entrar fora de hora; vantagem tática pequena. Can cast/enter as reaction; +1 Initiative bonus."},

    "Defender":      {"cost": 0.5, "cr_offense": -0.50, "cr_defense": 0.25, "dpr_bonus": -1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "mechanism": "Limiting (Can't Attack)",
                      "notes": "Não pode atacar normalmente; papel de tanque/segurador. Cannot use melee attacks; immune to forced movement."},

    # Ravnica-specific / blocks
    "Forecast":      {"cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Pequeno efeito ativado no início do turno; utilitário contínuo."},

    "Radiance":      {"cr_offense": 1.00, "cr_defense": 0.0, "dpr_bonus": 3.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Efeito que se espalha — transforma alvo único em múltiplos alvos. Use com cuidado: pode ser +1 CR quando afeta 2+ alvos."},

    "Transmute":     {"cr_offense": 0.20, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Troca de efeitos (utility); pouco impacto direto no CR."},

    "Dredge":        {"cr_offense": 0.10, "cr_defense": 1.00, "dpr_bonus": 0.5, "hp_delta": 10, "save_dc_delta": 0,
                      "notes": "Recursão de habilidades: aumenta resiliência, adicionar HP plano para refletir recuperação; escalável."},

    "Bloodthirst":   {"cr_offense": 0.50, "cr_defense": 0.0, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Entra em combate com bônus se um oponente foi ferido — situacional, use quando apropriado."},

    "Replicate":     {"cr_offense": 1.00, "cr_defense": 0.0, "dpr_bonus": 3.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Copiar um efeito aumenta DPR efetivo; cada cópia adicional soma DPR estimado."},

    "Haunt":         {"cr_offense": 0.60, "cr_defense": 0.40, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 1,
                      "notes": "Efeito retardado/recorrente — aumenta ofensa e resistência por triggers futuros."},

    "Hellbent":      {"cr_offense": 0.50, "cr_defense": -0.25, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Bonus forte com mão vazia (condicional). Use como bônus situacional."},

    "Convoke":       {"cr_offense": 0.30, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Habilidade de reduzir custos — utilitária, favorece força em grupo."},

    "Graft":         {"cr_offense": 0.40, "cr_defense": 0.40, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Contadores que podem ser redistribuídos; aumenta durabilidade e sinergia."},

    "Detain":        {"cr_offense": 1.00, "cr_defense": 0.50, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 2,
                      "notes": "Bloqueio de permanent: forte controle — aplicar CD de resistência para o alvo."},

    "Battalion":     {"cr_offense": 0.60, "cr_defense": 0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Dispara com ataque em grupo (3 ou mais atacantes) — sinergia."},

    "Cipher":        {"cr_offense": 1.50, "cr_defense": 0.0, "dpr_bonus": 5.0, "hp_delta": 0, "save_dc_delta": 1,
                      "notes": "Repetição de feitiços ao causar dano — potencial de loop ofensivo elevado."},

    "Scavenge":      {"cr_offense": 0.25, "cr_defense": 0.60, "dpr_bonus": 0.5, "hp_delta": 5, "save_dc_delta": 0,
                      "notes": "Exilar criatura do cemitério para buff; tanto utilitário quanto defensivo."},

    "Bloodrush":     {"cr_offense": 0.45, "cr_defense": -0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Discard-to-buff; bom para combos, situacional."},

    "Overload":      {"cr_offense": 1.50, "cr_defense": -0.25, "dpr_bonus": 4.0, "hp_delta": 0, "save_dc_delta": 1,
                      "notes": "Transforma alvo em AoE; muito poderoso em multi-alvo."},

    "Extort":        {"cr_offense": 0.20, "cr_defense": 0.20, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Pequeno drain ao conjurar; acumula com múltiplos casts."},

    "Unleash":       {"cr_offense": 0.50, "cr_defense": -0.50, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "+1/+1 ao entrar; não pode bloquear se tem o marcador — trade-off ataque/defesa."},

    "Populate":      {"cr_offense": 0.50, "cr_defense": 0.40, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Cria tokens — aumenta presença em campo e valor tático."},

    "Evolve":        {"cr_offense": 0.45, "cr_defense": 0.45, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Escala com entrada de criaturas maiores; bom em jogos longos."},

    "Addendum":      {"cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Bônus se usado na main phase; pequena vantagem estratégica."},

    "Mentor":        {"cr_offense": 0.25, "cr_defense": 0.10, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Coloca +1/+1 em aliados menores; melhora ataques de small minions."},

    "Surveil":       {"cr_offense": 0.15, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Manipulação de topo de deck/efeitos futuros — utilitário."},

    "Undergrowth":   {"cr_offense": 0.50, "cr_defense": 0.50, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Escala fortemente com número de cards de criatura no cemitério; aplicar escala dinâmica."},

    "Riot":          {"cr_offense": 0.50, "cr_defense": 0.10, "dpr_bonus": 2.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Escolha entre +1/+1 ou haste — útil e simples."},

    "Jump-start":    {"cr_offense": 0.40, "cr_defense": 0.0, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Permite reusar feitiços do cemitério com custo; aumenta DPR em jogadas longas."},

    "Afterlife":     {"cr_offense": 0.35, "cr_defense": 0.60, "dpr_bonus": 1.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Spawn de tokens ao morrer — acrescenta resistência via substitutos."},

    "Spectacle":     {"cr_offense": 0.40, "cr_defense": 0.0, "dpr_bonus": 1.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Custo alternativo se um oponente perdeu vida — situacionalmente poderoso."},

    "Convoke":       {"cr_offense": 0.30, "cr_defense": 0.10, "dpr_bonus": 0.0, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Permite gastar recursos aliados para pagar custos — utilitário de grupo."},

    "Adapt":         {"cr_offense": 0.25, "cr_defense": 0.25, "dpr_bonus": 0.5, "hp_delta": 0, "save_dc_delta": 0,
                      "notes": "Pagamento por counters; pequeno buff por recurso."},
}

# ==========================================================
# RARITY MULTIPLIERS & FILE PATHS (unchanged)
# ==========================================================

RARITY_MULTIPLIERS = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "mythic": 5,
}

# File paths - using pathlib for cross-platform compatibility
from pathlib import Path
_PROJECT_ROOT = Path(__file__).parent.parent
_DATA_SOURCE = _PROJECT_ROOT / "data" / "source"
_DATA_OUTPUT = _PROJECT_ROOT / "data" / "output"
_DATA_TEMP = _PROJECT_ROOT / "data" / "temp"

INPUT_MONSTERS_FILE = str(_DATA_SOURCE / "monsters.json")
INPUT_RAVNICA_FILE = str(_DATA_SOURCE / "ravnicaCreatures.json")
OUTPUT_MONSTERS_FILE = str(_DATA_OUTPUT / "finalMonsters.json")
OUTPUT_RAVNICA_FILE = str(_DATA_OUTPUT / "final.json")
NEW_TYPES_LOG_FILE = str(_DATA_TEMP / "newTypes.txt")

# ==========================================================
# Helper notes for implementers (não-executável)
# ==========================================================
# Recomendações de uso:
# - Ao converter uma carta, some todos os cr_offense e cr_defense dos traits aplicáveis.
# - Converta o CR base estimado pela heurística (CMC, P/T, raridade) e então aplique os ajustes:
#       cr_final_offense = cr_base_offense + sum(trait.cr_offense)
#       cr_final_defense = cr_base_defense + sum(trait.cr_defense)
#   Depois combine em CR final (média ou usando DMG method: média entre ofensivo e defensivo).
#
# - Ajustes de DPR: some dpr_bonus para estimar DPR final. Use isso para calcular CR ofensivo
#   ou para ajustar ataques/feitiços/uso de perícias.
#
# - Ajustes de HP: aplique hp_delta e hp_multiplier aos HP base calculados.
#
# - Save/DC: se uma keyword define um save, use:
#       save_dc = 8 + CR_bonus_equivalente + relevant_attribute_mod
#   Onde "CR_bonus_equivalente" pode ser CHALLENGE_RATINGS[str(rounded_CR)]["bonus"].
#
# - Para habilidades situacionais (ex: Bloodthirst, Hellbent), aplique apenas quando as condições são atendidas.
#
# Exemplo de pipeline simplificado (pseudo):
#   base = estimate_cr_from_cmc_and_pt(card)
#   offense = base["offense"]
#   defense = base["defense"]
#   for trait in card_traits:
#       offense += KEYWORD_BALANCE[trait]["cr_offense"]
#       defense += KEYWORD_BALANCE[trait]["cr_defense"]
#       dpr += KEYWORD_BALANCE[trait]["dpr_bonus"]
#       hp += KEYWORD_BALANCE[trait]["hp_delta"]
#   final_cr = round_to_nearest_CR(average(offense, defense))
#
# ==========================================================
# TRAIT COST BUDGETS (CR-based complexity limits)
# ==========================================================
# Máximo de "points de complexidade" de traits que uma criatura pode ter conforme CR.
# Higher CR = more complex traits allowed. This prevents CR 1 goblins from having 5 traits.
# Traits applied should have their costs summed and not exceed the budget for the CR.
#
# "cost" field in KEYWORD_BALANCE and COLOR_TRAIT_BALANCE defines how many points a trait uses.
# Reduced/lite versions: (Lite) suffix, cost = ceil(full_cost / 2)
#
TRAIT_BUDGETS = {
    0: 1,      # CR 0-1: max 1 point (no traits or 1 very simple)
    1: 1,
    2: 2,      # CR 2: max 2 points (simple trait)
    3: 3,      # CR 3-5: max 3 points (1-2 traits)
    4: 3,
    5: 4,
    6: 4,      # CR 6-8: max 4-5 points (2-3 traits or 1 powerful)
    7: 5,
    8: 5,
    9: 6,      # CR 9-12: max 6-7 points (multiple traits)
    10: 7,
    11: 7,
    12: 7,
    13: 8,     # CR 13+: up to 8+ points (legendary complexity)
    14: 8,
    15: 9,
    16: 9,
    17: 10,
    18: 10,
    19: 11,
    20: 11,
    21: 12,
    22: 12,
    23: 13,
    24: 13,
    25: 14,
    26: 14,
    27: 15,
    28: 15,
    29: 16,
    30: 16,
}

def get_trait_budget(cr: float) -> int:
    """Return max trait complexity points allowed for a given CR."""
    cr_int = int(cr)
    if cr_int in TRAIT_BUDGETS:
        return TRAIT_BUDGETS[cr_int]
    elif cr_int < 0:
        return TRAIT_BUDGETS[0]
    else:
        return TRAIT_BUDGETS[30]  # fallback for very high CRs

# Isso oferece um sistema balanceado e auditável para ajustar automaticamente o CR
# e gerar stat blocks 5e coerentes com o sabor e as mecânicas de MTG.