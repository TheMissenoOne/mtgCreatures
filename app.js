import { readFile, writeFile } from "fs/promises";
const cards = JSON.parse(
  await readFile(new URL("./ravnicaCreatures.json", import.meta.url))
);
const monsters = JSON.parse(
  await readFile(new URL("./monsters.json", import.meta.url))
);

const rarity = {
  common: 1,
  uncommon: 2,
  rare: 3,
  mythic: 5,
};

const baseStats = [
  {
    Challenge: "1/8 (25 XP)",
    "Armor Class": 13,
    "Hit Points": 15,
    bonus: 2,
    DC: 13,
  },
  {
    Challenge: "1/4 (50 XP)",
    "Armor Class": 13,
    "Hit Points": 20,
    bonus: 2,
    DC: 13,
  },
  {
    Challenge: "1/2 (100 XP)",
    "Armor Class": 13,
    "Hit Points": 30,
    bonus: 3,
    DC: 13,
  },
  {
    Challenge: "1 (200 XP)",
    "Armor Class": 13,
    "Hit Points": 40,
    bonus: 3,
    DC: 13,
  },
  {
    Challenge: "2 (450 XP)",
    "Armor Class": 13,
    "Hit Points": 50,
    bonus: 3,
    DC: 13,
  },
  {
    Challenge: "3 (700 XP)",
    "Armor Class": 14,
    "Hit Points": 65,
    bonus: 4,
    DC: 13,
  },
  {
    Challenge: "4 (1100 XP)",
    "Armor Class": 14,
    "Hit Points": 80,
    bonus: 4,
    DC: 14,
  },
  {
    Challenge: "5 (1800 XP)",
    "Armor Class": 15,
    "Hit Points": 95,
    bonus: 4,
    DC: 15,
  },
  {
    Challenge: "6 (2300 XP)",
    "Armor Class": 15,
    "Hit Points": 110,
    bonus: 4,
    DC: 15,
  },
  {
    Challenge: "7 (2900 XP)",
    "Armor Class": 15,
    "Hit Points": 130,
    bonus: 5,
    DC: 15,
  },
  {
    Challenge: "8 (3900 XP)",
    "Armor Class": 16,
    "Hit Points": 150,
    bonus: 5,
    DC: 16,
  },
  {
    Challenge: "9 (5000 XP)",
    "Armor Class": 16,
    "Hit Points": 170,
    bonus: 5,
    DC: 16,
  },
  {
    Challenge: "10 (5900 XP)",
    "Armor Class": 17,
    "Hit Points": 200,
    bonus: 5,
    DC: 16,
  },
  {
    Challenge: "11 (7200 XP)",
    "Armor Class": 17,
    "Hit Points": 220,
    bonus: 5,
    DC: 17,
  },
  {
    Challenge: "12 (8400 XP)",
    "Armor Class": 17,
    "Hit Points": 240,
    bonus: 6,
    DC: 18,
  },
  {
    Challenge: "13 (10000 XP)",
    "Armor Class": 18,
    "Hit Points": 260,
    bonus: 6,
    DC: 18,
  },
  {
    Challenge: "14 (11500 XP)",
    "Armor Class": 18,
    "Hit Points": 280,
    bonus: 6,
    DC: 18,
  },
  {
    Challenge: "15 (13000 XP)",
    "Armor Class": 18,
    "Hit Points": 300,
    bonus: 6,
    DC: 18,
  },
  {
    Challenge: "16 (15000 XP)",
    "Armor Class": 18,
    "Hit Points": 320,
    bonus: 6,
    DC: 18,
  },
  {
    Challenge: "17 (18000 XP)",
    "Armor Class": 19,
    "Hit Points": 330,
    bonus: 6,
    DC: 19,
  },
  {
    Challenge: "18 (20000 XP)",
    "Armor Class": 19,
    "Hit Points": 350,
    bonus: 6,
    DC: 19,
  },
  {
    Challenge: "19 (22000 XP)",
    "Armor Class": 19,
    "Hit Points": 370,
    bonus: 7,
    DC: 19,
  },
  {
    Challenge: "20 (25000 XP)",
    "Armor Class": 19,
    "Hit Points": 400,
    bonus: 7,
    DC: 19,
  },
];

const keywords = {
  Counter:
    "Counter a Spell Whenever this effect triggers, the creturecreates a 15 foot antimagic cube centered on a point it cansee within 30 ",
  Cycle:
    "Cycle When this creature has advantage it may give up thatadvantage to perferm the effct listed when you cycle thiscard. If there is no effect listed then this creature gainsinspiration at the end of their turn",
  Deathtouch:
    "Deathtouch At the beginning of this creature's second turnthey coat their weapons and body in poison. Until thebeginning of their next turn any time they are hit with amelee attack they deal Xd6 poison damage to theirattacker. Where X is this creature's CR. Also until thebeginning of their next turn all attacks the creature makesdeal an extra 1d6 poison damage on hit",
  Defender:
    "Defender This creature cannot take the attack actionnormally on their turn. When this creature is attacked theymay make an atack action targetting its attacker",
  Destroy:
    "Destroy When the condition on the card is met, this monstermay force a creature to make a dexterity 15 saving throw. On a failed save the creature takes Xd10 damage where Xis this monster's CR. On a sucessful save the creaturetakes half as much damage",
  Discard:
    "Discard When the condition on the card is met this creatureimposes disadvantage on the next, attack roll, ability checkor save made by one creature",
  Draw: "Draw When the condition on the card is met, this creaturegains inspiration",
  "Double Strike":
    "DoubleStrike As a reaction to an enemy creature enteringthis creatures melee range, this creature may spend theirreaction to make up to two melee attacks against thecreature that entered",
  Fight:
    "Fight When the condition on the card is met this creaturemay choose an enemy within its movement range. It maythen move to that enemy and make one mele attack againstthem",
  "First Strike":
    "First Strike As a reaction to an enemy creature entering thiscreatures melee range, this creature may spend theirreaction to make one melee attack against the creaturethat entered",
  Flash:
    "Flash When the GM is determining surprise, if this creatureis not surprised, then all enemy combantants becomesurprised",
  Flying:
    "Flying Has a Flying speed Equal to Its movement Speed, if ithasn't attacked this round it does not provoke opportunityattacks",
  Haste:
    "Haste This creature has avdantage on initiative rolls, andadvantage on each attack it makes in the first round ofcombat",
  Hexproof:
    "Hexproof This creature has advantage on saving throwsagainst magical effects and resistence to magical damage",
  Indestructible:
    "Indestructible This creature has immunity to bludgeoning piercing or slashing damage from non-magical weapons and resistence to those damage types from magicalweapons",
  Lifelink:
    "Lifelink As a bonus action, this creature may invoke its lifedraining properties. The next time it deals damage thisturn, it gains that much life",
  Menace:
    "MenaceAt the beginning of its turn, as a bonus action if thecreature has half HP or less, it lets out a menacing aura",
  Creatures:
    "Creatures within 30 feet must make a Wisdom savingthrow or be frightened for one minute. Creatures whosucceed this save are immune to this effect for 24 hours",
  Protection:
    "Protection As if indestructible with respect to source writtenon the card",
  Reach:
    "Reach +5 feet to melee range. If the creature has hit with amelee attack on a non-adjacent creature this turn, it maymake another melee attack of the same type as a bonusaction",
  Trample:
    "Trample As a bonus action, this creature may move up to itsmovement speed, moving through creatures as if theyweren't there. Any creature moved through in this waymakes a Dexterity saving throw or takes 1d4 bludgeoningdamage a number of times equal to the creature's CR",
  Vigilance:
    "Vigilance Whenever this creature makes a successful attackof opportunity, it regains the use of its reaction",
  Mutate:
    "Mutate The creature can, as an action, give its mutate triggeras a benefit to another willing creature it can see within60feet",
  Tap: "Tap Chosen creature makes a saving throw (whatever abilityyou think is pertinent) versus this monsters Save DC or isknocked prone",
};

let filteredCards = cards.map((element) => {
  if (
    (element != null,
    element?.type_line?.split(" — ")[0] === "Creature" &&
      (element?.set_name.toLowerCase().includes("ravnica") ||
        element?.set_name.toLowerCase().includes("guild") ||
        element?.set_name.toLowerCase().includes("dissension") ||
        element?.set_name.toLowerCase().includes("dragon's maze") ||
        element?.set_name.toLowerCase().includes("war of the spark") ||
        element?.set_name.toLowerCase().includes("gatecrash")))
  ) {
    return element?.type_line
      .split(" — ")[1]
      .split(" ")
      .map((type) => {
        if (
          type != undefined &&
          !JSON.stringify(monsters)
            .toLowerCase()
            .includes(type.toLowerCase())
        ) {
          return type;
        }
      });
  }
});

console.log(filteredCards)
let listOfTypes = [filteredCards[0]];
filteredCards.forEach((element) => {
  if(element?.length){
    element?.forEach((type)=>{
      if(!listOfTypes.includes(type)){
        listOfTypes = listOfTypes.concat(type);
      }
    })
  }else{
    if(!listOfTypes.includes(element)){
      listOfTypes = listOfTypes.concat(element);
    }
  }
 
  
});

writeFile(
  "ravnicaCreaturesTypes.json",
  JSON.stringify(listOfTypes),
  "utf8",
  () => {}
);

// const types = JSON.parse(
//   await readFile(new URL("./ravnicaCreaturesTypes.json", import.meta.url))
// );

// writeFile(
//   "finalTypes.json",
//   JSON.stringify(
//     types.map((element, index) => {
//       if (!types.slice(0, index).includes(element)) {
//         return element;
//       }
//     })
//   ),
//   "utf8",
//   () => {}
// );

//   {
//     console.log(cards[i].name);
//     let types = cards[i]?.type_line.split(" — ")[1].split(" ");
//     console.log(types);
//     // console.log(cards[i]);
//     console.log(rarity[cards[i].rarity]);
//     console.log(cards[i].power + "/" + cards[i].toughness);
//     console.log(cards[i].oracle_text);
//     console.log(
//       Math.round(
//         Math.log(
//           rarity[cards[i].rarity] /
//             (cards[i].cmc / (cards[i].power + cards[i].toughness))
//         ) + cards[i].cmc
//       )
//     );
//     let creature =
//       baseStats[
//         Math.round(
//           Math.log(
//             rarity[cards[i].rarity] /
//               (cards[i].cmc / (cards[i].power + cards[i].toughness))
//           ) + cards[i].cmc
//         )
//       ];
//     console.log(creature);
//   }
// }