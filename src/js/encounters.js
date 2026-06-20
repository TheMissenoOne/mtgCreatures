let CREATURES_DATABASE = null;
let _encounterCreaturesData = [];
let _usedCreatureNames = new Set();

const GUILD_COLORS = {
    azorius: ["W", "U"],
    dimir:   ["U", "B"],
    rakdos:  ["B", "R"],
    golgari: ["B", "G"],
    selesnya:["G", "W"],
    orzhov:  ["W", "B"],
    izzet:   ["U", "R"],
    gruul:   ["R", "G"],
    boros:   ["R", "W"],
    simic:   ["U", "G"],
};

const ENVIRONMENTS = {
    // Single guild
    azorius: {
        name: "Azorius Administrative District",
        subtitle: "Courts, infinite archives, and enforcement precincts",
        guilds: ["azorius"],
        threat: "Arrest warrants, magical binding, and asset seizure.",
        hooks: [
            "The party is summoned to answer for a legal violation they may not have committed.",
            "A dissident is detained without trial — someone wants them silenced before the hearing.",
            "A Lawmage has gone rogue and is rewriting city ordinances to consolidate power.",
        ]
    },
    orzhov: {
        name: "Orzhov Cathedral Vault",
        subtitle: "Gilded basilicas that serve as banks, churches, and debtors' prisons",
        guilds: ["orzhov"],
        threat: "Debt binding, spectral enforcers, and centuries-old contracts.",
        hooks: [
            "A debt the party did not know they owed has been called in, with compound interest.",
            "A ghost thrall is attempting to break free from its service contract and needs protection.",
            "The Orzhov want something retrieved from their own sealed lower vault, which they dare not enter.",
        ]
    },
    izzet: {
        name: "Izzet Research Laboratory",
        subtitle: "Volatile towers of experimental thaumaturgy",
        guilds: ["izzet"],
        threat: "Containment breach, magical overload, and collateral detonation.",
        hooks: [
            "A portal experiment has fused two laboratory wings and something came through.",
            "A mage has been conducting unauthorized memory extraction on unwilling subjects.",
            "A new weapon prototype has gone fully active and the mage who built it is missing.",
        ]
    },
    rakdos: {
        name: "Rakdos Performance Arena",
        subtitle: "Blood theater, sadistic spectacle, and ritual carnival grounds",
        guilds: ["rakdos"],
        threat: "Audience frenzy, performers who kill for sport, and ritual chaos.",
        hooks: [
            "The party has been volunteered as tonight's featured act without their knowledge.",
            "A Rakdos performer is harboring a fugitive and the guild leadership does not know.",
            "The ringmaster's latest ritual is drawing on something far older than the Cult.",
        ]
    },
    selesnya: {
        name: "Selesnya Conclave Garden",
        subtitle: "Vast living oases sheltering tens of thousands of willing members",
        guilds: ["selesnya"],
        threat: "Forced communion, psychic merging, and collective enforcement.",
        hooks: [
            "Pilgrims are vanishing inside the garden. The Conclave says they simply joined the chorus.",
            "A dryad elder has gone silent and the grove around her is visibly dying.",
            "The Conclave is mobilizing an unusually large force and will not say why.",
        ]
    },
    golgari: {
        name: "Golgari Undercity Necropolis",
        subtitle: "Fungal warrens and undead-living ecosystems beneath the streets",
        guilds: ["golgari"],
        threat: "Necrophagous swarms, rot shambler awakenings, and reclamation rites.",
        hooks: [
            "A body the party is searching for has already been reclaimed, revived, and deployed.",
            "The Golgari are preparing a great Rot Harvest and are short on raw material.",
            "A section of the necropolis has been sealed. Nothing enters. Nothing leaves.",
        ]
    },
    simic: {
        name: "Simic Zonot Research Hub",
        subtitle: "Deep-water biomes and mutation chambers operated by the Combine",
        guilds: ["simic"],
        threat: "Unstable hybrids, accelerated evolution, and predator containment failure.",
        hooks: [
            "A krasis has been sighted moving through the city canal system toward the surface.",
            "A researcher has fused with their experiment and the process cannot be reversed.",
            "The Combine is offering free augmentation to debtors. The procedure is irreversible.",
        ]
    },
    gruul: {
        name: "Gruul Clan Territory",
        subtitle: "Overgrown ruins, smashed infrastructure, and contested wild zones",
        guilds: ["gruul"],
        threat: "Clan raids, beast stampedes, and ritual combat challenges.",
        hooks: [
            "A Gruul shaman claims the land beneath a city block is sacred and will prove it tonight.",
            "Something is driving the clans into the city in unprecedented numbers.",
            "A young chieftain wants to negotiate peace. The elder clans intend to stop them.",
        ]
    },
    boros: {
        name: "Boros Legion Garrison",
        subtitle: "Military precincts and armored fortresses of the angelic legion",
        guilds: ["boros"],
        threat: "Martial law, angel-commanded strikes, and collateral enforcement.",
        hooks: [
            "The garrison is on full alert after an armory theft and the party is considered suspect.",
            "A Boros captain has gone off-order and is executing civilians without sanction.",
            "Legion soldiers are disappearing from their posts. No bodies, no signs of struggle.",
        ]
    },
    dimir: {
        name: "Dimir Safe House",
        subtitle: "Subterranean cells, forbidden libraries, and shadow networks",
        guilds: ["dimir"],
        threat: "Infiltration, memory theft, and assassination before dawn.",
        hooks: [
            "The party holds information the Dimir believe only they should possess.",
            "A known spy has offered to defect, but every handler they contact turns up dead.",
            "Someone is selling Dimir intelligence. The guild wants the seller found before the buyer does.",
        ]
    },
    // Multi-guild locations
    undercity: {
        name: "Undercity Passages",
        subtitle: "Contested fungal tunnels where Dimir and Golgari interests collide",
        guilds: ["dimir", "golgari"],
        threat: "Memory-stealing fog, rot-creature patrols, and flooded dead ends.",
        hooks: [
            "A sealed chamber has been breached. Both guilds want what is inside and neither will say what it is.",
            "Something is moving through the lower tunnels that is neither Dimir nor Golgari work.",
            "A cartographer has gone missing with the only complete map of the lower passages.",
        ]
    },
    steam_vents: {
        name: "Industrial Ruins",
        subtitle: "Izzet-abandoned workshops now claimed by Gruul clans",
        guilds: ["izzet", "gruul"],
        threat: "Unstable magitech traps, territorial beasts, and volatile residue.",
        hooks: [
            "An Izzet prototype weapon was left behind when the lab was abandoned. The Gruul have figured out how to use it.",
            "The ruins sit on a power conduit the Izzet need reclaimed. The Gruul will not move.",
            "Something buried under the workshop floor is waking up.",
        ]
    },
    sacred_foundry: {
        name: "Military Forge District",
        subtitle: "Boros-Izzet joint forges producing weapons and armor for the Legion",
        guilds: ["boros", "izzet"],
        threat: "Experimental ordnance, angel-supervised security, and internal sabotage.",
        hooks: [
            "A weapons shipment has been redirected. Both guilds blame each other.",
            "An Izzet modification to standard Legion armor has been quietly killing soldiers.",
            "The party must escort a prototype weapon through a forge district under active assault.",
        ]
    },
    watery_grave: {
        name: "Flooded Crypts",
        subtitle: "Drowned Orzhov vaults where Dimir archivists pick through the secrets of the dead",
        guilds: ["dimir", "orzhov"],
        threat: "Trapped spirits, flooded corridors, and layered wards protecting buried leverage.",
        hooks: [
            "A debt ledger sealed in a flooded vault could expose both guilds. Both want it destroyed.",
            "The ghost of a high-ranking prelate will not rest and is revealing Dimir secrets in its ravings.",
            "A missing Dimir agent was last seen entering an Orzhov crypt. That was three days ago.",
        ]
    },
    dead_streets: {
        name: "Debt Quarter",
        subtitle: "Orzhov-controlled streets where Golgari reclaim the abandoned dead",
        guilds: ["orzhov", "golgari"],
        threat: "Spectral debt collectors, rot shambler patrols, and binding contracts enforced by force.",
        hooks: [
            "The Orzhov are harvesting their own indebted dead before the Golgari can claim the bodies.",
            "A living debtor has accepted Golgari sanctuary. The Orzhov have sent collectors.",
            "An entire street has been sealed off with no explanation. Locals say the dead walk there at night.",
        ]
    },
    breeding_pool: {
        name: "Simic-Izzet Hybridization Lab",
        subtitle: "Joint experimental facility where biological and arcane science collide",
        guilds: ["simic", "izzet"],
        threat: "Failed hybrids, arcane feedback loops, and escaped test subjects.",
        hooks: [
            "A joint experiment has produced something neither guild designed. It is still growing.",
            "Test subjects have developed a shared intelligence and are coordinating an escape.",
            "The facility's lead researcher has gone silent. Their final log entry reads: It works. Do not come in.",
        ]
    },
    precinct_six: {
        name: "Sixth District Chaos Zone",
        subtitle: "Lower city blocks where Rakdos carnivals and Gruul incursions converge",
        guilds: ["rakdos", "gruul"],
        threat: "Mob violence, performer attacks, and clan-carnival territorial clashes.",
        hooks: [
            "A Rakdos parade and a Gruul raid arrived at the same city block at the same time.",
            "Someone has been hiring Gruul as muscle for Rakdos performances and paying in stolen weapons.",
            "A Gruul elder and a Rakdos demon are both claiming the same ancient ruin as sacred ground.",
        ]
    },
    tenth_district: {
        name: "Tenth District Streets",
        subtitle: "The most populated district in Ravnica, contested by Boros, Azorius, and Selesnya",
        guilds: ["boros", "azorius", "selesnya"],
        threat: "Civilian crossfire, competing guild jurisdiction, and public order collapse.",
        hooks: [
            "Three guild patrols converge on the same block, each carrying conflicting orders.",
            "A public gathering has been infiltrated by a guild agent. No one agrees which guild sent them.",
            "A building collapse has trapped civilians and the guilds are arguing over jurisdiction rather than helping.",
        ]
    },
    sunhome: {
        name: "Sunhome Fortress",
        subtitle: "The Boros Legion's great central stronghold and command center",
        guilds: ["boros"],
        threat: "Angelic command authority, fortress lockdown, and Legion rapid response.",
        hooks: [
            "Someone has breached Sunhome's inner sanctum. The angels have sealed the fortress.",
            "A holy relic kept in Sunhome has started producing effects no one can identify or stop.",
            "A high-ranking angel has issued orders that contradict Legion doctrine. No one dares question it.",
        ]
    },
    ravnica_plaza: {
        name: "Open Market District",
        subtitle: "Neutral ground where all guilds trade, spy, and scheme in plain sight",
        guilds: ["any"],
        threat: "Anything. Every guild maintains a presence here.",
        hooks: [
            "A public assassination has occurred and every guild has a different suspect in mind.",
            "Stolen goods from multiple guilds are surfacing at the same merchant stall.",
            "The market has been placed under Azorius quarantine. No one will say why.",
        ]
    },
};

// =============================================================
// Synergy classification system
// Tags are lowercased to match normalized keyword/type data.
// =============================================================

const SYNERGY_GROUPS = [
    { label: "Legion Strike Force",   tags: ["battalion", "soldier", "knight", "mentor", "first strike"] },
    { label: "Aerial Assault",        tags: ["flying", "bird", "drake", "flash", "vigilance"] },
    { label: "Savage Hunt",           tags: ["trample", "haste", "riot", "bloodthirst", "bloodrush", "beast"] },
    { label: "Undead Horde",          tags: ["afterlife", "zombie", "spirit", "scavenge"] },
    { label: "Mutagenic Vanguard",    tags: ["evolve", "adapt", "proliferate", "insect", "elemental"] },
    { label: "Shadow Network",        tags: ["surveil", "mill", "rogue", "deathtouch"] },
    { label: "Nature's Wardens",      tags: ["defender", "reach", "lifelink", "elf", "druid"] },
    { label: "Berserker Warband",     tags: ["unleash", "haste", "berserker", "goblin"] },
    { label: "Spectral Congregation", tags: ["afterlife", "spirit", "extort", "convoke", "cleric"] },
    { label: "Shamanic Circle",       tags: ["shaman", "elf", "druid", "bloodrush"] },
    { label: "Arcane Cabal",          tags: ["wizard", "vedalken", "adapt", "surveil"] },
    { label: "Warrior Warband",       tags: ["warrior", "human", "mentor", "vigilance"] },
    { label: "Debt Collectors",       tags: ["extort", "vampire", "thrull", "specter"] },
    { label: "Spectacle of Carnage",  tags: ["unleash", "menace", "demon", "devil", "berserker"] },
    { label: "Aerial Guard",          tags: ["flying", "vigilance", "reach", "defender"] },
];

// Extract creature subtypes from MTG type_line (text after '—')
function getCreatureSubtypes(data) {
    const line = data.type_line || '';
    const dash = line.indexOf(' — ');
    if (dash < 0) return [];
    return line.slice(dash + 3).split(' ').filter(Boolean);
}

// Build a normalized tag set for a creature (keywords + subtypes, lowercase)
function creatureTags(c) {
    return new Set([
        ...(c.data.keywords || []).map(k => k.toLowerCase()),
        ...getCreatureSubtypes(c.data).map(t => t.toLowerCase()),
    ]);
}

// Score synergy between two encounter creatures (higher = more thematic)
function scoreSynergy(a, b) {
    let score = 0;
    const tagsA = creatureTags(a);
    const tagsB = creatureTags(b);

    // Shared creature subtypes
    for (const t of tagsA) {
        if (tagsB.has(t)) score += 3;
    }

    // Same guild/color combination
    const colA = (a.colors || []).slice().sort().join('');
    const colB = (b.colors || []).slice().sort().join('');
    if (colA === colB && colA) score += 2;

    // Synergy group overlap
    for (const group of SYNERGY_GROUPS) {
        const aHits = group.tags.filter(t => tagsA.has(t)).length;
        const bHits = group.tags.filter(t => tagsB.has(t)).length;
        if (aHits > 0 && bHits > 0) score += Math.min(aHits, bHits) * 2;
    }

    return score;
}

// Identify the dominant synergy theme for a group of selected creatures
function classifyEncounterGroup(selected) {
    const allTags = new Set();
    for (const c of selected) {
        for (const t of creatureTags(c)) allTags.add(t);
    }
    let best = null;
    let bestOverlap = 1; // require at least 2 tag matches
    for (const group of SYNERGY_GROUPS) {
        const overlap = group.tags.filter(t => allTags.has(t)).length;
        if (overlap > bestOverlap) { bestOverlap = overlap; best = group; }
    }
    return best;
}

// Weighted random pick from a pool
function pickWeightedRandom(pool, weightFn) {
    const total = pool.reduce((s, c) => s + weightFn(c), 0);
    if (total <= 0) return pool[Math.floor(Math.random() * pool.length)];
    let r = Math.random() * total;
    for (const c of pool) { r -= weightFn(c); if (r <= 0) return c; }
    return pool[pool.length - 1];
}

const CR_XP_VALUES = {
    0: 10, "1/8": 25, "1/4": 50, "1/2": 100,
    1: 200, 2: 450, 3: 700, 4: 1100,
    5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900,
    11: 7200, 12: 8400, 13: 10000, 14: 11500, 15: 13000,
    16: 15000, 17: 18000, 18: 20000, 19: 22000, 20: 25000,
    21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000,
    26: 90000, 27: 105000, 28: 120000, 29: 135000, 30: 155000
};

function xpForCR(numericCR, rawCRStr) {
    // Try exact string key first ("1/4", "1/2", "1/8")
    if (rawCRStr && CR_XP_VALUES[rawCRStr] !== undefined) return CR_XP_VALUES[rawCRStr];
    // Then integer key
    const rounded = Math.round(numericCR);
    return CR_XP_VALUES[rounded] || 100;
}

async function loadCreatures() {
    if (CREATURES_DATABASE) return CREATURES_DATABASE;
    try {
        const response = await fetch('../data/output/final.json');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        CREATURES_DATABASE = await response.json();
        return CREATURES_DATABASE;
    } catch (error) {
        console.error('Error loading creatures:', error);
        return null;
    }
}

// Convert colors array to lowercase guild key: ['W', 'U'] => 'azorius'
function colorsToGuild(colors) {
    if (!colors || colors.length !== 2) return null;
    const sorted = [...colors].sort().join('');
    const map = {
        'UW': 'azorius', 'BU': 'dimir', 'BR': 'rakdos',
        'BG': 'golgari', 'GW': 'selesnya', 'BW': 'orzhov',
        'RU': 'izzet', 'GR': 'gruul', 'RW': 'boros', 'GU': 'simic'
    };
    return map[sorted] || null;
}

// Extract numeric CR and raw CR string from challenge string
function parseCR(challengeStr) {
    if (!challengeStr) return { num: 0, raw: '0' };
    const match = challengeStr.match(/^([\d/\.]+)/);
    if (!match) return { num: 0, raw: '0' };
    const raw = match[1];
    if (raw.includes('/')) {
        const [a, b] = raw.split('/');
        return { num: parseInt(a) / parseInt(b), raw };
    }
    return { num: parseFloat(raw), raw };
}

function filterCreaturesForEnvironment(creatures, envKey, minCR, maxCR) {
    const env = ENVIRONMENTS[envKey];
    if (!env) return [];

    const guilds = env.guilds;
    const anyGuild = guilds.includes('any');

    // Build set of all single colors belonging to this environment's guilds
    const envColors = new Set();
    if (!anyGuild) {
        for (const g of guilds) {
            (GUILD_COLORS[g] || []).forEach(c => envColors.add(c));
        }
    }

    const filtered = [];
    for (const creature of Object.values(creatures)) {
        const { num: cr, raw: rawCR } = parseCR(creature.Challenge);
        if (cr < minCR || cr > maxCR) continue;

        const colors = creature.colors || [];
        let matches = anyGuild;

        if (!matches) {
            const creatureGuild = colorsToGuild(colors);
            if (creatureGuild && guilds.includes(creatureGuild)) {
                matches = true;
            } else if (colors.length === 1 && envColors.has(colors[0])) {
                matches = true;
            }
        }

        if (matches) {
            filtered.push({
                data: creature,
                name: creature.name,
                cr,
                rawCR,
                challenge: creature.Challenge,
                xp: xpForCR(cr, rawCR),
                colors,
            });
        }
    }
    return filtered;
}

function calculateThresholds(partyLevel, partySize) {
    const xpByLevel = {
        1:  { easy: 25,   medium: 50,   hard: 75,   deadly: 100   },
        2:  { easy: 50,   medium: 100,  hard: 150,  deadly: 200   },
        3:  { easy: 75,   medium: 150,  hard: 225,  deadly: 400   },
        4:  { easy: 125,  medium: 250,  hard: 375,  deadly: 500   },
        5:  { easy: 250,  medium: 500,  hard: 750,  deadly: 1100  },
        6:  { easy: 300,  medium: 600,  hard: 900,  deadly: 1400  },
        7:  { easy: 350,  medium: 750,  hard: 1100, deadly: 1700  },
        8:  { easy: 450,  medium: 900,  hard: 1400, deadly: 2100  },
        9:  { easy: 550,  medium: 1100, hard: 1600, deadly: 2400  },
        10: { easy: 600,  medium: 1200, hard: 1900, deadly: 2800  },
        11: { easy: 800,  medium: 1600, hard: 2400, deadly: 3600  },
        12: { easy: 1000, medium: 2000, hard: 3000, deadly: 4500  },
        13: { easy: 1100, medium: 2200, hard: 3300, deadly: 5100  },
        14: { easy: 1250, medium: 2500, hard: 3800, deadly: 5700  },
        15: { easy: 1400, medium: 2800, hard: 4200, deadly: 6300  },
        16: { easy: 1600, medium: 3200, hard: 4800, deadly: 7200  },
        17: { easy: 2000, medium: 3900, hard: 5900, deadly: 9500  },
        18: { easy: 2100, medium: 4200, hard: 6300, deadly: 9500  },
        19: { easy: 2400, medium: 4900, hard: 7300, deadly: 9500  },
        20: { easy: 2800, medium: 5700, hard: 8500, deadly: 10900 },
    };
    const baseXp = xpByLevel[Math.min(Math.max(partyLevel, 1), 20)];
    const m = partySize / 4;
    return {
        easy:   Math.floor(baseXp.easy   * m),
        medium: Math.floor(baseXp.medium * m),
        hard:   Math.floor(baseXp.hard   * m),
        deadly: Math.floor(baseXp.deadly * m),
    };
}

function selectRandomDifficulty() {
    const opts = ["easy", "medium", "hard", "deadly"];
    const weights = [3, 5, 4, 2];
    const total = weights.reduce((a, b) => a + b, 0);
    let r = Math.random() * total;
    for (let i = 0; i < opts.length; i++) {
        r -= weights[i];
        if (r <= 0) return opts[i];
    }
    return "medium";
}

function formatDifficulty(d) {
    return { easy: "Easy", medium: "Medium", hard: "Hard", deadly: "Deadly" }[d] || d;
}

function randomHook(env) {
    if (!env.hooks || !env.hooks.length) return null;
    return env.hooks[Math.floor(Math.random() * env.hooks.length)];
}

async function selectCreaturesForEncounter(envKey, targetXP, partyLevel, partySize, difficulty) {
    const creatures = await loadCreatures();
    if (!creatures) return [];

    const crMult = { easy: 0.5, medium: 1, hard: 1.5, deadly: 2 }[difficulty] || 1;
    const baseCR = partyLevel * crMult;
    // Wider variance = bigger pool = more variety across rolls
    const variance = 2.5 + partyLevel / 4;
    const minCR = Math.max(0, baseCR - variance);
    const maxCR = baseCR + variance;

    let pool = filterCreaturesForEnvironment(creatures, envKey, minCR, maxCR);
    // Widen CR window if pool is thin
    if (pool.length < 5) pool = filterCreaturesForEnvironment(creatures, envKey, 0, 30);
    if (!pool.length)    pool = filterCreaturesForEnvironment(creatures, 'ravnica_plaza', minCR, maxCR);
    if (!pool.length)    return [];

    // Deduplicate by name (defensive guard)
    const seen = new Set();
    pool = pool.filter(c => { if (seen.has(c.name)) return false; seen.add(c.name); return true; });

    // Penalize creatures used earlier this session to maximise variety
    const weight = c => _usedCreatureNames.has(c.name) ? 0.15 : 1.0;

    // Pick a seed creature via weighted random (prefers un-used creatures)
    const seed = pickWeightedRandom(pool, weight);

    // Score every other candidate: synergy with seed + jitter + usage penalty
    const candidates = pool
        .filter(c => c.name !== seed.name)
        .map(c => ({
            creature: c,
            score: scoreSynergy(seed, c) * 2
                   + Math.random() * 1.5
                   - (_usedCreatureNames.has(c.name) ? 3 : 0),
        }))
        .sort((a, b) => b.score - a.score);

    // Max creature count scales with party size
    const maxCount = Math.max(2, Math.min(6, Math.round(partySize * 1.25)));

    // Greedy XP-budget fill, synergy-first
    const selected = [seed];
    let totalXP = seed.xp;

    for (const { creature } of candidates) {
        if (selected.length >= maxCount) break;
        if (totalXP + creature.xp <= targetXP * 1.5) {
            selected.push(creature);
            totalXP += creature.xp;
        }
    }

    // If budget was too tight, pad with cheapest available to reach at least 2
    if (selected.length < 2) {
        const byXP = [...pool].sort((a, b) => a.xp - b.xp);
        for (const c of byXP) {
            if (!selected.find(s => s.name === c.name)) {
                selected.push(c);
                if (selected.length >= 2) break;
            }
        }
    }

    // Track used names; reset after 30 distinct creatures so creatures recycle eventually
    selected.forEach(c => _usedCreatureNames.add(c.name));
    if (_usedCreatureNames.size > 30) _usedCreatureNames.clear();

    return selected;
}

async function generateEncounter() {
    const envSelect = document.getElementById("environment");
    const partySize = parseInt(document.getElementById("partySize").value) || 4;
    const partyLevel = parseInt(document.getElementById("partyLevel").value) || 1;
    const difficultySelect = document.getElementById("difficulty").value;

    if (!envSelect.value) {
        alert("Select an environment first.");
        return;
    }

    let envKey = envSelect.value;
    if (envKey === "random") {
        const keys = Object.keys(ENVIRONMENTS);
        envKey = keys[Math.floor(Math.random() * keys.length)];
    }

    const env = ENVIRONMENTS[envKey];
    const difficulty = difficultySelect === "random" ? selectRandomDifficulty() : difficultySelect;
    const thresholds = calculateThresholds(partyLevel, partySize);
    const targetXP = thresholds[difficulty];

    const creatures = await selectCreaturesForEncounter(envKey, targetXP, partyLevel, partySize, difficulty);
    const totalXP = creatures.reduce((s, c) => s + c.xp, 0);
    const adjustedXP = Math.round(totalXP * (partySize / 4));
    const hook = randomHook(env);
    const synergyGroup = classifyEncounterGroup(creatures);

    _encounterCreaturesData = creatures;

    const creaturesHTML = creatures.map((c, i) => {
        const artUrl = c.data.image_uris?.art_crop || '';
        const thumbStyle = artUrl
            ? `background-image:url(${artUrl});background-size:cover;background-position:center top;`
            : 'background:#1c2230;';
        const subtypes = getCreatureSubtypes(c.data).slice(0, 3).join(' · ');
        const keywords = (c.data.keywords || []).slice(0, 3).join(', ');
        const tagsLine = [subtypes, keywords].filter(Boolean).join(' — ');
        return `<div class="encounter-card" onclick="toggleStatBlock(this,${i})">
            <div class="encounter-card-header">
                <div class="encounter-card-thumb" style="${thumbStyle}"></div>
                <div class="encounter-card-info">
                    <strong>${c.name}</strong>
                    <div class="encounter-card-meta">CR ${c.rawCR} &bull; ${c.xp} XP</div>
                    ${tagsLine ? `<div class="encounter-card-tags">${tagsLine}</div>` : ''}
                </div>
                <span class="expand-arrow">&#9660;</span>
            </div>
            <div class="statblock-expand" style="display:none;margin-top:12px;"></div>
        </div>`;
    }).join('');

    const html = `
        <div class="result-env">
            <div class="result-env-name">${env.name}</div>
            <div class="result-env-sub">${env.subtitle}</div>
        </div>
        ${hook ? `<div class="result-hook"><span class="result-hook-label">Adventure Hook</span>${hook}</div>` : ''}
        <div class="result-section">
            <div class="result-section-label">Encounter Creatures</div>
            <div class="encounters-grid">${creaturesHTML}</div>
        </div>
        <div class="result-section result-stats">
            <div class="result-section-label">Statistics</div>
            <div class="stat-row">
                <span class="stat-item"><span class="stat-key">Raw XP</span>${totalXP}</span>
                <span class="stat-item"><span class="stat-key">Adjusted (${partySize} players)</span>${adjustedXP}</span>
                <span class="stat-item"><span class="stat-key">${difficulty.toUpperCase()} threshold</span>${targetXP} XP</span>
            </div>
            <div class="stat-threat"><span class="stat-key">Threat</span>${env.threat}</div>
        </div>
        <div class="result-footer">
            <span class="difficulty-indicator difficulty-${difficulty}">${formatDifficulty(difficulty)}</span>
            ${synergyGroup ? `<span class="synergy-badge">${synergyGroup.label}</span>` : ''}
            <span class="footer-party">${partySize} players &bull; Level ${partyLevel}</span>
            <button class="reroll-btn" onclick="generateEncounter()">Roll Again</button>
        </div>
    `;

    document.getElementById("encounterTitle").textContent = `Encounter — ${env.name}`;
    document.getElementById("encounterContent").innerHTML = html;
    document.getElementById("encounterResult").classList.add("visible");
    setTimeout(() => {
        document.getElementById("encounterResult").scrollIntoView({ behavior: "smooth" });
    }, 100);
}

function openCreaturesTab() {
    window.location.href = "../index.html";
}

function toggleStatBlock(card, idx) {
    const expand = card.querySelector('.statblock-expand');
    const arrow = card.querySelector('.expand-arrow');
    if (!expand) return;
    if (expand.style.display === 'none') {
        const c = _encounterCreaturesData[idx];
        if (!c) return;
        const d = c.data;
        const ac = d['Armor Class'] ?? '10';
        const hp = d['Hit Points'] ?? '10';
        const speed = d['Speed'] || '30 ft.';
        const str = d.STR ?? '10'; const dex = d.DEX ?? '10'; const con = d.CON ?? '10';
        const int = d.INT ?? '10'; const wis = d.WIS ?? '10'; const cha = d.CHA ?? '10';
        const senses = d.Senses || 'Passive Perception 10';
        const languages = d.Languages || '—';
        const skills = d.Skills || '—';
        const challenge = d.Challenge || '0 (0 XP)';
        const traits = d.Traits || '';
        const actions = d.Actions || '<p><em>No actions listed</em></p>';
        let imm = '';
        if (d['Damage Immunities']) imm += `<property-line><h4>Damage Immunities</h4><p>${d['Damage Immunities']}</p></property-line>`;
        if (d['Damage Resistances']) imm += `<property-line><h4>Damage Resistances</h4><p>${d['Damage Resistances']}</p></property-line>`;
        if (d['Condition Immunities']) imm += `<property-line><h4>Condition Immunities</h4><p>${d['Condition Immunities']}</p></property-line>`;
        expand.innerHTML = `<stat-block>
          <creature-heading><h1>${d.name}</h1><h2>${d.meta || ''}</h2></creature-heading>
          <top-stats>
            <property-line><h4>Armor Class</h4><p>${ac}</p></property-line>
            <property-line><h4>Hit Points</h4><p>${hp}</p></property-line>
            <property-line><h4>Speed</h4><p>${speed}</p></property-line>
            <abilities-block data-str="${str}" data-dex="${dex}" data-con="${con}" data-int="${int}" data-wis="${wis}" data-cha="${cha}"></abilities-block>
            ${imm}
            <property-line><h4>Senses</h4><p>${senses}</p></property-line>
            <property-line><h4>Languages</h4><p>${languages}</p></property-line>
            <property-line><h4>Skills</h4><p>${skills}</p></property-line>
            <property-line><h4>Challenge</h4><p>${challenge}</p></property-line>
          </top-stats>
          ${traits}<h3>Actions</h3>${actions}
        </stat-block>`;
        expand.style.display = 'block';
        if (arrow) arrow.textContent = '▲';
    } else {
        expand.style.display = 'none';
        if (arrow) arrow.textContent = '▼';
    }
}

// Populate environment description on select change
function onEnvironmentChange() {
    const key = document.getElementById("environment").value;
    const box = document.getElementById("envDescription");
    if (!box) return;
    if (!key || key === 'random' || !ENVIRONMENTS[key]) {
        box.style.display = 'none';
        return;
    }
    const env = ENVIRONMENTS[key];
    const guildsLabel = env.guilds.includes('any') ? 'All guilds' :
        env.guilds.map(g => g.charAt(0).toUpperCase() + g.slice(1)).join(' + ');
    box.innerHTML = `<div class="env-desc-name">${env.name}</div>
        <div class="env-desc-sub">${env.subtitle}</div>
        <div class="env-desc-guilds">Guilds: ${guildsLabel}</div>`;
    box.style.display = 'block';
}

document.addEventListener("keypress", e => {
    if (e.key === "Enter") generateEncounter();
});

window.addEventListener('load', () => {
    document.getElementById("environment").addEventListener("change", onEnvironmentChange);
    loadCreatures().then(data => {
        if (data) console.log(`${Object.keys(data).length} creatures loaded`);
    });
});
