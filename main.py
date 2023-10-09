import json
import math
from fractions import Fraction
import re


challenge = {
    "0": {
        "Challenge": "0 (10 XP)",
        "Armor Class": 10,
        "Hit Points": 10,
        "bonus": 1,
        "DC": 10,
    },
    "1/8": {
        "Challenge": "1/8 (25 XP)",
        "Armor Class": 13,
        "Hit Points": 15,
        "bonus": 2,
        "DC": 13,
    },
    "1/4": {
        "Challenge": "1/4 (50 XP)",
        "Armor Class": 13,
        "Hit Points": 20,
        "bonus": 2,
        "DC": 13,
    },
    "1/2": {
        "Challenge": "1/2 (100 XP)",
        "Armor Class": 13,
        "Hit Points": 30,
        "bonus": 3,
        "DC": 13,
    },
    "1": {
        "Challenge": "1 (200 XP)",
        "Armor Class": 13,
        "Hit Points": 40,
        "bonus": 3,
        "DC": 13,
    },
    "2": {
        "Challenge": "2 (450 XP)",
        "Armor Class": 13,
        "Hit Points": 50,
        "bonus": 3,
        "DC": 13,
    },
    "3": {
        "Challenge": "3 (700 XP)",
        "Armor Class": 14,
        "Hit Points": 65,
        "bonus": 4,
        "DC": 13,
    },
    "4": {
        "Challenge": "4 (1100 XP)",
        "Armor Class": 14,
        "Hit Points": 80,
        "bonus": 4,
        "DC": 14,
    },
    "5": {
        "Challenge": "5 (1800 XP)",
        "Armor Class": 15,
        "Hit Points": 95,
        "bonus": 4,
        "DC": 15,
    },
    "6": {
        "Challenge": "6 (2300 XP)",
        "Armor Class": 15,
        "Hit Points": 110,
        "bonus": 4,
        "DC": 15,
    },
    "7": {
        "Challenge": "7 (2900 XP)",
        "Armor Class": 15,
        "Hit Points": 130,
        "bonus": 5,
        "DC": 15,
    },
    "8": {
        "Challenge": "8 (3900 XP)",
        "Armor Class": 16,
        "Hit Points": 150,
        "bonus": 5,
        "DC": 16,
    },
    "9": {
        "Challenge": "9 (5000 XP)",
        "Armor Class": 16,
        "Hit Points": 170,
        "bonus": 5,
        "DC": 16,
    },
    "10": {
        "Challenge": "10 (5900 XP)",
        "Armor Class": 17,
        "Hit Points": 200,
        "bonus": 5,
        "DC": 16,
    },
    "11": {
        "Challenge": "11 (7200 XP)",
        "Armor Class": 17,
        "Hit Points": 220,
        "bonus": 5,
        "DC": 17,
    },
    "12": {
        "Challenge": "12 (8400 XP)",
        "Armor Class": 17,
        "Hit Points": 240,
        "bonus": 6,
        "DC": 18,
    },
    "13": {
        "Challenge": "13 (10000 XP)",
        "Armor Class": 18,
        "Hit Points": 260,
        "bonus": 6,
        "DC": 18,
    },
    "14": {
        "Challenge": "14 (11500 XP)",
        "Armor Class": 18,
        "Hit Points": 280,
        "bonus": 6,
        "DC": 18,
    },
    "15": {
        "Challenge": "15 (13000 XP)",
        "Armor Class": 18,
        "Hit Points": 300,
        "bonus": 6,
        "DC": 18,
    },
    "16": {
        "Challenge": "16 (15000 XP)",
        "Armor Class": 18,
        "Hit Points": 320,
        "bonus": 6,
        "DC": 18,
    },
    "17": {
        "Challenge": "17 (18000 XP)",
        "Armor Class": 19,
        "Hit Points": 330,
        "bonus": 6,
        "DC": 19,
    },
    "18": {
        "Challenge": "18 (20000 XP)",
        "Armor Class": 19,
        "Hit Points": 350,
        "bonus": 6,
        "DC": 19,
    },
    "19": {
        "Challenge": "19 (22000 XP)",
        "Armor Class": 19,
        "Hit Points": 370,
        "bonus": 7,
        "DC": 19,
    },
    "20": {
        "Challenge": "20 (25000 XP)",
        "Armor Class": 19,
        "Hit Points": 400,
        "bonus": 7,
        "DC": 19,
    },
    "21": {
        "Challenge": "21 (33000 XP)",
        "Armor Class": 20,
        "Hit Points": 450,
        "bonus": 7,
        "DC": 20,
    },
    "22": {
        "Challenge": "22 (41000 XP)",
        "Armor Class": 20,
        "Hit Points": 500,
        "bonus": 7,
        "DC": 20,
    },
    "23": {
        "Challenge": "23 (50000 XP)",
        "Armor Class": 20,
        "Hit Points": 550,
        "bonus": 8,
        "DC": 21,
    },
    "24": {
        "Challenge": "24 (62000 XP)",
        "Armor Class": 21,
        "Hit Points": 600,
        "bonus": 8,
        "DC": 21,
    },
    "25": {
        "Challenge": "25 (75000 XP)",
        "Armor Class": 21,
        "Hit Points": 650,
        "bonus": 8,
        "DC": 21,
    },
    "26": {
        "Challenge": "26 (90000 XP)",
        "Armor Class": 21,
        "Hit Points": 700,
        "bonus": 8,
        "DC": 21,
    },
    "27": {
        "Challenge": "27 (105000 XP)",
        "Armor Class": 22,
        "Hit Points": 800,
        "bonus": 8,
        "DC": 22,
    },
    "28": {
        "Challenge": "28 (120000 XP)",
        "Armor Class": 22,
        "Hit Points": 900,
        "bonus": 9,
        "DC": 22,
    },
    "29": {
        "Challenge": "29 (135000 XP)",
        "Armor Class": 22,
        "Hit Points": 1000,
        "bonus": 9,
        "DC": 22,
    },
    "30": {
        "Challenge": "30 (155000 XP)",
        "Armor Class": 22,
        "Hit Points": 1100,
        "bonus": 9,
        "DC": 23,
    }
}



attributes = [
    "STR",
    "DEX",
    "CON",
    "INT",
    "WIS",
    "CHA",]

types = ["Viashino","Shaman","Drake","Vedalken","Nephilim","Advisor","Mutant","Leviathan","Soldier","Archon","Bird","Griffin","Barbarian","Wurm","Archer","Thrull","Jellyfish","Shade","Shapeshifter","Dinosaur","Phoenix","Slug","Antelope","Sheep","Minion","Fish","Praetor","Hellion","Monk","Pilot","Lammasu","Mercenary"]

colors=traits = {
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
keywords = {
  "Counter": "<property-block><h4>Counter a Spell.</h4><p>Whenever this effect triggers, the creturecreates a 15 foot antimagic cube centered on a point it cansee within 30 </p></property-block>",
  "Cycle": "<property-block><h4>Cycle.</h4><p>When this creature has advantage it may give up thatadvantage to perferm the effct listed when you cycle thiscard. If there is no effect listed then this creature gainsinspiration at the end of their turn</p></property-block>",
  "Deathtouch": "<property-block><h4>Deathtouch.</h4><p>At the beginning of this creature's second turnthey coat their weapons and body in poison. Until thebeginning of their next turn any time they are hit with amelee attack they deal Xd6 poison damage to theirattacker. Where X is this creature's CR. Also until thebeginning of their next turn all attacks the creature makesdeal an extra 1d6 poison damage on hit</p></property-block>",
  "Defender": "<property-block><h4>Defender.</h4><p>This creature cannot take the attack actionnormally on their turn. When this creature is attacked theymay make an atack action targetting its attacker</p></property-block>",
  "Destroy": "<property-block><h4>Destroy.</h4><p>When the condition on the card is met, this monstermay force a creature to make a dexterity 15 saving throw. On a failed save the creature takes Xd10 damage where Xis this monster's CR. On a sucessful save the creaturetakes half as much damage</p></property-block>",
  "Discard": "<property-block><h4>Discard.</h4><p>When the condition on the card is met this creatureimposes disadvantage on the next, attack roll, ability checkor save made by one creature</p></property-block>",
  "Draw": "Draw When the condition on the card is met, this creaturegains inspiration</p></property-block>",
  "Double Strike": "<property-block><h4>DoubleStrike.</h4><p>As a reaction to an enemy creature enteringthis creatures melee range, this creature may spend theirreaction to make up to two melee attacks against thecreature that entered</p></property-block>",
  "Fight": "<property-block><h4>Fight.</h4><p>When the condition on the card is met this creaturemay choose an enemy within its movement range. It maythen move to that enemy and make one mele attack againstthem</p></property-block>",
  "First Strike": "<property-block><h4>First.</h4><p>Strike As a reaction to an enemy creature entering thiscreatures melee range, this creature may spend theirreaction to make one melee attack against the creaturethat entered</p></property-block>",
  "Flash": "<property-block><h4>Flash.</h4><p>When the GM is determining surprise, if this creatureis not surprised, then all enemy combantants becomesurprised</p></property-block>",
  "Flying": "<property-block><h4>Flying.</h4><p>Has a Flying speed Equal to Its movement Speed, if ithasn't attacked this round it does not provoke opportunityattacks</p></property-block>",
  "Haste": "<property-block><h4>Haste.</h4><p>This creature has avdantage on initiative rolls, andadvantage on each attack it makes in the first round ofcombat</p></property-block>",
  "Hexproof": "<property-block><h4>Hexproof.</h4><p>This creature has advantage on saving throwsagainst magical effects and resistence to magical damage</p></property-block>",
  "Indestructible": "<property-block><h4>Indestructible.</h4><p>This creature has immunity to bludgeoning piercing or slashing damage from non-magical weapons and resistence to those damage types from magicalweapons</p></property-block>",
  "Lifelink": "<property-block><h4>Lifelink.</h4><p>As a bonus action, this creature may invoke its lifedraining properties. The next time it deals damage thisturn, it gains that much life</p></property-block>",
  "Menace": "<property-block><h4>MenaceAt.</h4><p>the beginning of its turn, as a bonus action if thecreature has half HP or less, it lets out a menacing aura</p></property-block>",
  "Creatures": "<property-block><h4>Creatures.</h4><p>within 30 feet must make a Wisdom savingthrow or be frightened for one minute. Creatures whosucceed this save are immune to this effect for 24 hours</p></property-block>",
  "Protection": "<property-block><h4>Protection.</h4><p>As if indestructible with respect to source writtenon the card</p></property-block>",
  "Reach": "<property-block><h4>Reach.</h4><p>+5 feet to melee range. If the creature has hit with amelee attack on a non-adjacent creature this turn, it maymake another melee attack of the same type as a bonusaction</p></property-block>",
  "Trample": "<property-block><h4>Trample.</h4><p>As a bonus action, this creature may move up to itsmovement speed, moving through creatures as if theyweren't there. Any creature moved through in this waymakes a Dexterity saving throw or takes 1d4 bludgeoningdamage a number of times equal to the creature's CR</p></property-block>",
  "Vigilance": "<property-block><h4>Vigilance.</h4><p>Whenever this creature makes a successful attackof opportunity, it regains the use of its reaction</p></property-block>",
  "Mutate": "<property-block><h4>Mutate.</h4><p>The creature can, as an action, give its mutate triggeras a benefit to another willing creature it can see within60feet</p></property-block>",
  "Tap":  "<property-block><h4>Tap.</h4><p>Chosen creature makes a saving throw (whatever abilityyou think is pertinent) versus this monsters Save DC or isknocked prone</p></property-block>",
  "Overload": "<property-block><h4>Overload.</h4><p>Whenever you upcast a spell by more than three levels, you may have it target any number of possible targets. If you cast an area of effect spell this way, you may have its center or travel to any number of targets to a maximum spell slot.</p></property-block>",
  "Replicate": "<property-block><h4>Replicate.</h4><p>Whenever you cast a spell, you may spend sorcery points equal to the level of the spell any number of times. Copy that spell for each time this cost was spent. If you cast a concentration spell this way, you may concentrate on any number of spells until the start of your next turn.</p></property-block>",
  "Jumpstart": "<property-block><h4>Jumpstart.</h4><p>For each spell level. in the next minute, you may, as a free action, cast a spell you have cast in the last hour.</p></property-block>",
  "Convoke": "<property-block><h4>Convoke.</h4><p>When casting a spell, any number of sentient beings may choose to give up their next bonus action; if they do, the spell costs one less spell level (you may cast spells you wouldn't have the appropriate level for this way)</p></property-block>",
  "Populate": "<property-block><h4>Populate.</h4><p>Once per short or long rest. Create an identical replica of an Animal companion or summoned creature. Any actions needed to command one may be used to command both. This creature dissipates after an hour or when killed.</p></property-block>",
  "Radiant": "<property-block><h4>Radiant.</h4><p>As a bonus action, choose an alignment and chose an effect that hasn't been chosen in the last hour.\n\nEach creature in range of chosen Alignment heals 1d8 hitpoints or takes 1d8 radiant hitpoints.\n\nEach creature of chosen Alignment gets the advantage on their next skill check or saving throw or gets disadvantage on their next skill check or saving throw.\n\nThe next time each player of chosen Alignment deals damage, they deal an extra 1d10 radiant damage or reduce their damage by 1d10.\n\nEach player of chosen Alignment gets ten extra feet of movement and may take a movement action as a bonus action until the end of their next turn or loses 10 feet of movement and cannot take movement actions until the end of their next turn.\n\nEach player of chosen Alignment either gains a extra reaction for 2 turns or losses their reaction for turns.</p></property-block>",
  "Battalion": "<property-block><h4>Battalion.</h4><p>Whenever you deal damage on an attack if two other leveled creatures deal damage with an attack to that same target. You may cast a spell with a level equivalent to half your proficiency modifier without spending a spell slot.</p></property-block>",
  "Mentor": "<property-block><h4>Mentor.</h4><p>Whenever you would deal damage with an attack, choose a target sentient creature and one of your stats. If that stat is greater than the chosen target equivalent stat, the chosen target adds 1d4 to that stat for 1 hour or until the creature falls unconscious.</p></property-block>",
  "Haunt": "<property-block><h4>Haunt.</h4><p>Whenever you would fall Unconscious, you choose a creature in sight range. They are haunted. Your spirit's location is theirs, and during their turn, you may cast cantrips and take bonus actions. If you would truly die or get resurrected, your spirit returns to your body/the afterlife.</p></property-block>",
  "Extort": "<property-block><h4>Extort.</h4><p>Whenever a d20 is rolled, you may spend (whatever is congruent to ten bucks in this setting). If you do, the money vanishes into the coffers of the ORZHOV, and target creature takes two damage, and the target creature heals 2</p></property-block>",
  "Afterlife": "<property-block><h4>Afterlife.</h4><p>whenever another player starts rolling death saves, you may create the 1/2 cr ghost; the fallen player commands this ghost during your turn. this ghost dissipates after 1 minute or until the player is back up. You can have up to half your proficiency modifier rounded down of these ghosts at one time.</p></property-block>",
  "Hellbent": "<property-block><h4>Hellbent.</h4><p>: Whenever you cast a spell using that level's last spell slot, you may choose any meta-magic effects. You may roll a performance check with a dc of 10 + the spell level + 5 per chosen effect - how cool your description is. If you succeed on the roll, you may cast the spell with all chosen effects without spending the cost.</p></property-block>",
  "Unleash": "<property-block><h4>Unleash.</h4><p>, at the beginning of combat, you may, for the next minute, deal an extra 1d8 per 5 paladin levels on hit and gain an advantage on all attacks. Still, all attacking enemies gain an advantage on attacks against you, and the dm tracks how many much damage your taking instead of you.</p></property-block>",
  "Spectacle": "<property-block><h4>Spectacle.</h4><p>: When you attack enemies that have taken more than ten damage since your last turn, you may roll performance and add your performance to the damage modifier. And when casting a spell, if the target has taken more than 10 damage, they either add or subtract your performance from their next roll,</p></property-block>",
  "Transmute": "<property-block><h4>Transmute.</h4><p>, you may take ten minutes to unlearn a spell. If you do, you may learn a spell from any spell list with a level equal to the base spell. You forget this spell after an hour. You may undo these effects in the shortest.</p></property-block>",
  "Cipher": "<property-block><h4>Cipher.</h4><p>chose a spell in secret and a creature in line of sight. If, in the next 30 minutes, that creature deals damage with a nonspell attack, you may cast the spell at a reduced spell level with no downsides. If no damage is dealt with within that time, you lose the original spell slot required to cast that spell. The slot reduction is equal to half your proficiency modifier rounded down. Calculating range as if you were at the chosen creature's position.</p></property-block>",
  "Surveil": "<property-block><h4>Surveil.</h4><p>Once per short rest, you may use your keen insight and foresight to survey your surroundings. You spend a few moments attuning to the ebb and flow of the aether, gaining insight into hidden truths. Roll a d20 and consult the table below:<p>- 1-5: You gain no additional information.</p><p>- 6-10: You gain a hint about a nearby danger or hidden passage.</p><p>- 11-15: You can sense magical auras, gaining advantage on the next Arcana check you make.</p><p>- 16-19: You receive a vision of a possible future, giving you advantage on the next Intelligence (Investigation) or Wisdom (Insight) check.</p><p>- 20: You glimpse into the beyond, receiving a cryptic message or vision that may guide your actions in the future.</p><p></p><p>The information received is at the discretion of the DM, and should be relevant to the current situation.</p></property-block>",
  "Forecast": "<property-block><h4>Forecast.</h4><p>A number of times equal to your proficiency modifier per long rest.As a bonus action. Name a spell you have prepared. All creatures in sight are aware you have this spell, and you can cast it. At any point before your next turn, you may cast the chosen spell with the minimum slot reduced by 2. All dice you roll in relation to this spell are instead replaced with the minimum possible roll.</p></property-block>",
  "Detain": "<property-block><h4>Detain.</h4><p>, whenever you would deal enough damage to drop a sentient creature to zero hitpoints, deal half or more of their max hp, you may instead cast hold the person or hold monster without spending a spell slot. They automatically fail their first saving throw.</p></property-block>",
  "Addendum": "<property-block><h4>Addendum.</h4><p>, Whenever you would cast the first spell that is castable on a reaction on your turn, you may cast if twice for the same spell slot.</p></property-block>",
  "Bloodthirst": "<property-block><h4>Bloodthirst.</h4><p>, Whenever a creature loses more than half its life, the creature who dealt that damage may choose a stat and roll d4s equal to half your proficiency modifier and add the total to the chosen stat.</p></property-block>",
  "Blood Rush": "<property-block><h4>Blood Rush.</h4><p>, whenever you or an ally attacks, you may use a reaction and a number of sorcery points equal to the spell level (cantrips are 0) to cast a spell targeting or centered on the Attacker, this spells minimum spell slot is reduced by your strength modifier to a minimum of 1.</p></property-block>",
  "Riot": "<property-block><h4>Riot.</h4><p>, At the beginning of combat, chose one. You get a surprise round before combat or roll d4s equal to half your proficiency modifier; add these numbers in any combination to your stat. If you choose dex, this doesn't affect the initiative.</p></property-block>",
  "Graft": "<property-block><h4>Graft.</h4><p>, At the beginning of combat, Add d4s to your Graph pool equal to your proficiency modifier. You may spend an action or a bonus action to roll one and add it to a stat for one minute. At the beginning of another player's turn, you may give them one of your dice for them to use as they choose.</p></property-block>",
  "Evolve": "<property-block><h4>Evolve.</h4><p>, The first time each hour, a friendly creature would make a roll and choose a stat; you make a d20 roll with a disadvantage by adding the chosen stat. If your roll was lower than the original roll, roll 1d4 and add the result to the chosen stat.</p></property-block>",
  "Adapt": "<property-block><h4>Adapt.</h4><p>, Lose a spell slot. Per level of that spell slot, you may add a d4 to any stat for the next hour and Choose any number of adaptations from the simic hybrid list; you may gain these abilities for the next hour. You may not activate these abilities until the last effects have faded or ended by choice.</p></property-block>",
  "Dredge": "<property-block><h4>Dredge.</h4><p>Whenever you fall unconscious, you may use a reaction to make the creature you see make a Constitution saving throw against your spell save dc. If they fail, they take necrotic damage equal to your proficiency modifier, and you gain that much life.</p></property-block>",
  "Scavenge": "<property-block><h4>Scavenge.</h4><p>Once per long rest, you may expend a spell slot of 1st level or higher to perform a Scavenge. You rummage through fallen foes, extracting vital essence. For each level of the expended spell slot, you may choose one of the following effects:\n\n- Gain temporary hit points equal to your spellcasting ability modifier plus the level of the expended spell slot.\n- Enhance one of your abilities temporarily. Choose one ability score and increase it by an amount equal to the level of the expended spell slot. This increase lasts for 1 hour.\n- Restore a used class feature or expendable resource, such as a channel divinity or racial trait.\n\nThe Scavenge ability must be used within 10 minutes of a creature's death. The expended spell slot is not used for any other purpose.</p></property-block>",
  "Undergrowth": "<property-block><h4>Undergrowth.</h4><p>Note each creature you can see that is reduced to 0 hit points, and choose one that hasn't been chosen since your last long rest... (rest of the description)</p></property-block>"
}


rarity = {
  "common": 1,
  "uncommon": 2,
  "rare": 3,
  "mythic": 5,
}


with open('monsters.json', encoding="utf8") as data_file:   
  creatureMods = {}
  creatures = json.load(data_file)
  for creature in creatures:
    creatureDifference = creature
    for cr in challenge.keys():
      if cr == creature['Challenge'].split(' ')[0]:
        if isinstance(creatureDifference["Armor Class"], str):
          creatureDifference["Armor Class"] = creatureDifference["Armor Class"].split(' ')[0]
        if isinstance(creatureDifference["Hit Points"], str):
          creatureDifference["Hit Points"] = creatureDifference["Hit Points"].split(' ')[0]
        for atribute in attributes:
          creatureDifference[atribute+"_mod"] = int(float(creature[atribute]) - (10 + Fraction(cr)*3/4))
          creatureDifference[atribute] =  10 +creatureDifference[atribute+"_mod"]                      
        creatureDifference["Armor Class"] = int(challenge[cr]["Armor Class"]) - int(creatureDifference["Armor Class"])
        creatureDifference["Hit Points"] = int(creatureDifference["Hit Points"])
        creatureMods[creatureDifference['name']] = creatureDifference  
        break 
  jsonCreatureMods = json.dumps(creatureMods)
  with open("finalMonsters.json", "w") as outfile:
    outfile.write(jsonCreatureMods)
    
with open('ravnicaCreatures.json', encoding="utf8") as data_file:   
    ravnicaCreatures = {}
    cards = json.load(data_file)
    for card in cards:
        if card["toughness"].isnumeric() and card["power"].isnumeric() and (float(card["power"]) + float(card["toughness"])) > 0:
          with open('finalMonsters.json', encoding="utf8") as data_file: 
            convertedCreature = card
            convertedCreature['Actions'] = ""
            convertedCreature['Languages'] = ""
            convertedCreature['Skills'] = ""
            convertedCreature['Senses'] = ""
            convertedCreature['Speed'] = ""
            convertedCreature['meta'] = ""
            convertedCreature['Damage Immunities'] = ""
            convertedCreature['Condition Immunities'] = ""
            convertedCreature['Damage Resistances'] = ""
            loadedCreatures = json.load(data_file)
            creatureCR = round(math.log(float(rarity[card["rarity"]]) / (float(card["cmc"]) / (float(card["power"]) + float(card["toughness"])))) + float(card["cmc"]))              
            types = list()
            for name in card['name'].split(" "):
              if name in loadedCreatures.keys():
                types.append(name)
              else:
                with open("newTypes.txt", "a") as outfile:
                  outfile.write( name+"\n")
            types = (card['type_line'].split(' — ')[1].split(" "))+ types
            for type in types:   
              if int(Fraction(loadedCreatures[type]["Challenge"].split(" ")[0])) > creatureCR:
                creatureCR =int( round((int(Fraction(loadedCreatures[type]["Challenge"].split(" ")[0])) + (creatureCR /5 ))))
              else:
                creatureCR =int( round((int( creatureCR + (Fraction(loadedCreatures[type]["Challenge"].split(" ")[0])/5)) )))
            convertedCreature.update(challenge[str(creatureCR)])
            if hasattr(card,"flavor_text"):
                convertedCreature["description"] = card["flavor_text"]
            for atribute in attributes:
              convertedCreature[atribute] = round( 10+ Fraction(convertedCreature['Challenge'].split(' ')[0])*3/4 )  
            for type in types :
              for atribute in attributes:
                if int(loadedCreatures[type][atribute]) > convertedCreature[atribute]:
                  convertedCreature[atribute] = int(loadedCreatures[type][atribute]) + round((convertedCreature[atribute]-10 )/4)
                else:
                  convertedCreature[atribute] = int(convertedCreature[atribute]) + round(int(loadedCreatures[type][atribute+"_mod"])/2)
              convertedCreature[atribute+"_mod"] = round((convertedCreature[atribute] -10)/2)
              convertedCreature["Hit Points"] = int((convertedCreature["Hit Points"] + loadedCreatures[type]["Hit Points"])/2)
              convertedCreature["Armor Class"] = convertedCreature["Armor Class"] + loadedCreatures[type]["Armor Class"]
              convertedCreature['Traits'] = card['oracle_text']
              # if card['type_line'].split(' — ')[1].split(" ")[0] == type and card['name'] == "Blood Operative":
              #   print(loadedCreatures[type])
              if "meta" in loadedCreatures[type] and card['type_line'].split(' — ')[1].split(" ")[0] == type :
                convertedCreature["meta"] = loadedCreatures[type]['meta']
              if "Senses" in loadedCreatures[type]:
                if loadedCreatures[type]["Senses"].split('., ')[0].split(" ")[0] != 'Passive':
                  # print(loadedCreatures[type]["Senses"].split(','))
                  for sense in loadedCreatures[type]["Senses"].split('., '): 
                    if sense == ' ' or  sense.strip().split(" ")[0].lower() == 'passive':
                      break
                    if sense.split(" ")[0] not in convertedCreature['Senses']:
                        convertedCreature['Senses'] = convertedCreature['Senses'] +", "+ sense
                    else:
                      for convertedSense in convertedCreature['Senses'].split('., ')[0]:
                        if  convertedSense.split(" ")[0] == sense.split(" ") and convertedSense.split(" ")[len(convertedSense.split(" "))-2] < sense.split(" ")[len(sense.split(" "))]:
                          convertedCreature['Senses'] = convertedCreature['Senses'].replace(convertedSense,sense)
              if 'Condition Immunities' in loadedCreatures[type]:
                  for conditionImunities in loadedCreatures[type]["Condition Immunities"].split('., '): 
                    if conditionImunities == ' ' or  conditionImunities.strip().split(" ")[0].lower() == 'passive':
                      break
                    if conditionImunities.split(" ")[0] not in convertedCreature['Condition Immunities']:
                        convertedCreature['Condition Immunities'] = convertedCreature['Condition Immunities'] +", "+ conditionImunities
                    else:
                      for convertedConditionsImmunities in convertedCreature['Condition Immunities'].split('., ')[0]:
                        if  convertedConditionsImmunities.split(" ")[0] == conditionImunities.split(" ") and convertedConditionsImmunities.split(" ")[len(convertedConditionsImmunities.split(" "))-2] < conditionImunities.split(" ")[len(conditionImunities.split(" "))]:
                          convertedCreature['Condition Immunities'] = convertedCreature['Condition Immunities'].replace(convertedConditionsImmunities,conditionImunities)
              if 'Damage Immunities' in loadedCreatures[type]:
                  for damageImunities in loadedCreatures[type]["Damage Immunities"].split('., '): 
                    if damageImunities == ' ' or  damageImunities.strip().split(" ")[0].lower() == 'passive':
                      break
                    if damageImunities.split(" ")[0] not in convertedCreature['Damage Immunities']:
                        convertedCreature['Damage Immunities'] = convertedCreature['Damage Immunities'] +", "+ damageImunities
                    else:
                      for convertedDamageImmunities in convertedCreature['Damage Immunities'].split('., ')[0]:
                        if  convertedDamageImmunities.split(" ")[0] == damageImunities.split(" ") and convertedDamageImmunities.split(" ")[len(convertedDamageImmunities.split(" "))-2] < damageImunities.split(" ")[len(damageImunities.split(" "))]:
                          convertedCreature['Damage Immunities'] = convertedCreature['Damage Immunities'].replace(convertedDamageImmunities,damageImunities)
              if 'Damage Resistances' in loadedCreatures[type]:
                  for damageResistance in loadedCreatures[type]["Damage Resistances"].split('., '): 
                    if damageResistance == ' ' or  damageResistance.strip().split(" ")[0].lower() == 'passive':
                      break
                    if damageResistance.split(" ")[0] not in convertedCreature['Damage Resistances']:
                        convertedCreature['Damage Resistances'] = convertedCreature['Damage Resistances'] +", "+ damageResistance
                    else:
                      for convertedDamageResistance in convertedCreature['Damage Resistances'].split('., ')[0]:
                        if  convertedDamageResistance.split(" ")[0] == damageResistance.split(" ") and convertedDamageResistance.split(" ")[len(convertedDamageResistance.split(" "))-2] < damageResistance.split(" ")[len(damageResistance.split(" "))]:
                          convertedCreature['Damage Resistances'] = convertedCreature['Damage Resistances'].replace(convertedDamageResistance,damageResistance)
              if "Speed" in loadedCreatures[type]:  
                  for speed in loadedCreatures[type]["Speed"].split('., '): 
                    if speed == ' ' or  speed.strip().split(" ")[0].lower() == 'passive':
                      break
                    if speed.split(" ")[0] not in convertedCreature['Speed']:
                        convertedCreature['Speed'] = convertedCreature['Speed'] +", "+ speed
                    else:
                      for convertedSpeed in convertedCreature['Speed'].split('., ')[0]:
                        if  convertedSpeed.split(" ")[0] == speed.split(" ") and convertedSpeed.split(" ")[len(convertedSpeed.split(" "))-2] < speed.split(" ")[len(speed.split(" "))]:
                          convertedCreature['Speed'] = convertedCreature['Speed'].replace(convertedSpeed,speed)
              if "Traits" in loadedCreatures[type]:
                for keyword in keywords.keys():
                  # convertedCreature["Traits"] = convertedCreature["Traits"].replace(keyword,keywords[keyword])
                  replaceObj = re.compile(re.escape(keyword), re.IGNORECASE)
                  convertedCreature["Traits"] = replaceObj.sub(keywords[keyword], convertedCreature["Traits"])
                convertedCreature["Traits"] = convertedCreature["Traits"] + loadedCreatures[type]["Traits"]
              if "Actions" in loadedCreatures[type]:
                  convertedCreature["Actions"] = convertedCreature["Actions"] + loadedCreatures[type]["Actions"]
              if "Languages" in loadedCreatures[type]:
                  convertedCreature["Languages"] = convertedCreature["Languages"] + loadedCreatures[type]["Languages"]
              if "Skills" in loadedCreatures[type]:
                if loadedCreatures[type]["Skills"].split(', ')[0].split(" ")[0] != 'Passive':
                  # print(loadedCreatures[type]["Skills"].split(','))
                  for skill in loadedCreatures[type]["Skills"].split(', '): 
                    if skill == ' ' or  skill.strip().split(" ")[0].lower() == 'passive':
                      break
                    if skill.split(" ")[0] not in convertedCreature['Skills']:
                        convertedCreature['Skills'] = convertedCreature['Skills'] +", "+ skill
                    else:
                      for convertedSkill in convertedCreature['Skills'].split(', ')[0]:
                        if  convertedSkill.split(" ")[0] == skill.split(" ") and convertedSkill.split("+")[1] < skill.split("+")[1]:
                          convertedCreature['Skills'] = convertedCreature['Skills'].replace(convertedSkill,skill)
              # if "Skills" in loadedCreatures[type]:
              #     convertedCreature["Skills"] = convertedCreature["Skills"] + loadedCreatures[type]["Skills"]    
              if hasattr(card,"watermark") and len(card['watermark']) in colors.keys():
                  convertedCreature['Traits'] = convertedCreature["Traits"] + colors["".join(card['watermark'])]
            ravnicaCreatures[convertedCreature['name']]=(convertedCreature)                     
        
jsonRavnicaCreatures = json.dumps(ravnicaCreatures)

with open("final.json", "w") as outfile:
    outfile.write(jsonRavnicaCreatures)