/**
 * Ravnica Card Type Extractor
 * Processes MTG Ravnica cards to identify missing creature types for lookup
 */

import { readFile, writeFile } from "fs/promises";

// Configuration
const CONFIG = {
  supportedSets: [
    "ravnica",
    "guild",
    "dissension",
    "dragon's maze",
    "war of the spark",
    "gatecrash",
  ],
  inputCardFile: "./ravnicaCreatures.json",
  inputMonstersFile: "./monsters.json",
  outputFile: "./ravnicaCreaturesTypes.json",
};

/**
 * Load JSON file with error handling
 */
async function loadJsonFile(filepath) {
  try {
    const data = await readFile(new URL(filepath, import.meta.url));
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error loading ${filepath}:`, error.message);
    return null;
  }
}

/**
 * Save JSON file with error handling
 */
async function saveJsonFile(filepath, data) {
  try {
    await writeFile(
      new URL(filepath, import.meta.url),
      JSON.stringify(data, null, 2),
      "utf8"
    );
    console.log(`✓ Saved to ${filepath}`);
  } catch (error) {
    console.error(`Error saving ${filepath}:`, error.message);
  }
}

/**
 * Check if a creature type is known in the base monster list
 */
function isKnownMonsterType(type, monsterData) {
  const monsterString = JSON.stringify(monsterData).toLowerCase();
  return monsterString.includes(type.toLowerCase());
}

/**
 * Extract creature types from Ravnica cards
 */
function extractCreatureTypes(cards, monsters) {
  const unknownTypes = new Set();
  const processedCards = [];

  cards.forEach((card) => {
    // Validate card structure
    if (!card || !card.type_line) {
      return;
    }

    // Check if it's from supported Ravnica sets
    const setName = (card.set_name || "").toLowerCase();
    const isSupportedSet = CONFIG.supportedSets.some((set) =>
      setName.includes(set)
    );

    if (!isSupportedSet) {
      return;
    }

    // Extract creature types from type line
    const typeLineParts = card.type_line.split(" — ");
    if (typeLineParts[0] !== "Creature" || !typeLineParts[1]) {
      return;
    }

    const cardTypes = typeLineParts[1].split(" ");

    // Identify unknown types
    cardTypes.forEach((type) => {
      if (type && !isKnownMonsterType(type, monsters)) {
        unknownTypes.add(type);
      }
    });

    processedCards.push(card);
  });

  return {
    unknownTypes: Array.from(unknownTypes).sort(),
    processedCount: processedCards.length,
  };
}

/**
 * Main execution
 */
async function main() {
  console.log("🔍 Extracting creature types from Ravnica cards...\n");

  // Load data files
  console.log("📂 Loading data files...");
  const cards = await loadJsonFile(CONFIG.inputCardFile);
  const monsters = await loadJsonFile(CONFIG.inputMonstersFile);

  if (!cards || !monsters) {
    console.error(
      "❌ Failed to load required files. Ensure both JSON files exist."
    );
    return;
  }

  console.log(`✓ Loaded ${cards.length} cards`);
  console.log(`✓ Loaded ${Object.keys(monsters).length} known creature types\n`);

  // Extract types
  console.log("🔎 Analyzing cards...");
  const { unknownTypes, processedCount } = extractCreatureTypes(
    cards,
    monsters
  );

  console.log(`✓ Processed ${processedCount} Ravnica creature cards`);
  console.log(
    `✓ Found ${unknownTypes.length} unknown creature types\n`
  );

  // Display results
  if (unknownTypes.length > 0) {
    console.log("📋 Unknown creature types:");
    unknownTypes.forEach((type) => console.log(`   - ${type}`));
  } else {
    console.log("✓ All creature types are recognized!");
  }

  // Save results
  await saveJsonFile(CONFIG.outputFile, unknownTypes);
  console.log(
    `\n✅ Analysis complete! Unknown types saved to ${CONFIG.outputFile}`
  );
}

// Run the script
main().catch(console.error);