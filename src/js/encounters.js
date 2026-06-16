let CREATURES_DATABASE = null;
let _encounterCreaturesData = [];

// Environment and thematic encounter data
const ENVIRONMENTS = {
    azorius: {
        name: "Azorius Administrative District",
        icon: "🏛️",
        description: "Government complexes, courts, infinite archives.",
        guilds: ["Azorius"],
        guildColors: [["W", "U"]],
        threat: "Audit, imprisonment, or asset seizure.",
    },
    orzhov: {
        name: "Orzhov Cathedral",
        icon: "⛪",
        description: "Luxurious basilicas that are banks, churches, and vaults.",
        guilds: ["Orzhov"],
        guildColors: [["W", "B"]],
        threat: "Debt collection, binding contracts.",
    },
    izzet: {
        name: "Izzet Laboratory",
        icon: "🧪",
        description: "Unstable and dangerous experimental towers.",
        guilds: ["Izzet"],
        guildColors: [["U", "R"]],
        threat: "Experiments spiraling disastrously out of control.",
    },
    rakdos: {
        name: "Rakdos Arena",
        icon: "🎭",
        description: "Theater, circus, ritual massacre.",
        guilds: ["Rakdos"],
        guildColors: [["B", "R"]],
        threat: "Chaos, sadistic performance, bloodshed.",
    },
    selesnya: {
        name: "Selesnya Garden",
        icon: "🌳",
        description: "Living oases within the city.",
        guilds: ["Selesnya"],
        guildColors: [["G", "W"]],
        threat: "Forced incorporation, communion ritual.",
    },
    golgari: {
        name: "Golgari Catacombs",
        icon: "☠️",
        description: "Necropolises, fungi, undead-living ecosystem.",
        guilds: ["Golgari"],
        guildColors: [["B", "G"]],
        threat: "Necrophagous swarms, the undead awaken.",
    },
    simic: {
        name: "Simic Zones",
        icon: "🧬",
        description: "Biological reserves and mutation chambers.",
        guilds: ["Simic"],
        guildColors: [["U", "G"]],
        threat: "Unstable hybrids and accelerated evolution.",
    },
    gruul: {
        name: "Gruul Territory",
        icon: "🪨",
        description: "Destroyed forests, ancient ruins, savagery.",
        guilds: ["Gruul"],
        guildColors: [["G", "R"]],
        threat: "Brute fury, wild beast, destruction.",
    },
    boros: {
        name: "Boros Garrison",
        icon: "",
        description: "Military fortresses, command post.",
        guilds: ["Boros"],
        guildColors: [["R", "W"]],
        threat: "Brutal enforcement of martial law.",
    },
    dimir: {
        name: "Dimir Cell",
        icon: "🕵️",
        description: "Hidden spaces, forbidden libraries.",
        guilds: ["Dimir"],
        guildColors: [["U", "B"]],
        threat: "Infiltration, secret assassination, stolen memories.",
    }
};

const GUILD_COLORS = {
    "Azorius": ["W", "U"],
    "Dimir": ["U", "B"],
    "Rakdos": ["B", "R"],
    "Golgari": ["B", "G"],
    "Selesnya": ["G", "W"],
    "Orzhov": ["W", "B"],
    "Izzet": ["U", "R"],
    "Gruul": ["R", "G"],
    "Boros": ["R", "W"],
    "Simic": ["U", "G"]
};

const CR_XP_VALUES = {
    0: 10, "1/8": 25, "1/4": 50, "1/2": 100, 1: 200, 2: 450, 3: 700, 4: 1100,
    5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000, 10: 5900, 11: 7200, 12: 8400,
    13: 10000, 14: 11500, 15: 13000, 16: 15000, 17: 18000, 18: 20000, 19: 22000,
    20: 25000, 21: 33000, 22: 41000, 23: 50000, 24: 62000, 25: 75000, 26: 90000,
    27: 105000, 28: 120000, 29: 135000, 30: 155000
};


async function loadCreatures() {
    if (CREATURES_DATABASE) return CREATURES_DATABASE;
    
    try {
        const response = await fetch('../data/output/final.json');
        CREATURES_DATABASE = await response.json();
        return CREATURES_DATABASE;
    } catch (error) {
        console.error('Error loading creatures:', error);
        return null;
    }
}

// Convert colors array to guild key: ['W', 'U'] => 'azorius'
function colorsToGuild(colors) {
    if (!colors || colors.length !== 2) return null;
    
    const sorted = colors.sort().join('');
    const colorCombos = {
        'UW': 'azorius', // sorted U,W
        'BU': 'dimir',  // B,U
        'BR': 'rakdos',
        'BG': 'golgari',
        'GW': 'selesnya',
        'BW': 'orzhov',
        'RU': 'izzet',  // sorted R,U
        'GR': 'gruul',
        'RW': 'boros',
        'GU': 'simic'
    };
    return colorCombos[sorted];
}

// Extract numeric CR from string like "8 (3900 XP)"
function parseCR(challengeStr) {
    if (!challengeStr) return 0;
    const match = challengeStr.match(/^([\d/\.]+)/);
    return match ? match[1] : '0';
}

// Filter creatures by guild and CR range
function filterCreaturesByGuildAndCR(creatures, guildKey, minCR, maxCR) {
    const filtered = [];
    
    // Mono-color creatures for each guild
    const guildMono = {
        'azorius': 'W', 'dimir': 'U', 'rakdos': 'B', 'golgari': 'G', 'selesnya': 'W',
        'orzhov': 'B', 'izzet': 'U', 'gruul': 'R', 'boros': 'R', 'simic': 'U'
    };
    
    for (const creature of Object.values(creatures)) {
        const colors = creature.colors || [];
        let matches = false;
        
        const creatureGuild = colorsToGuild(colors);
        if (creatureGuild === guildKey) {
            matches = true;
        } else if (colors.length === 1) {
            const guildColor = guildMono[guildKey];
            if (colors[0] === guildColor) {
                matches = true;
            }
        }
        
        if (matches) {
            const cr = parseFloat(parseCR(creature.Challenge));
            if (cr >= minCR && cr <= maxCR) {
                filtered.push({
                    data: creature,
                    name: creature.name,
                    cr: cr,
                    challenge: creature.Challenge,
                    xp: CR_XP_VALUES[cr] || 100,
                    colors: colors,
                    traits: creature.Traits || ""
                });
            }
        }
    }
    
    return filtered;
}

// Calculate XP thresholds by level and party size
function calculateThresholds(partyLevel, partySize) {
    const xpByLevel = {
        1: { easy: 25, medium: 50, hard: 75, deadly: 100 },
        2: { easy: 50, medium: 100, hard: 150, deadly: 200 },
        3: { easy: 75, medium: 150, hard: 225, deadly: 400 },
        4: { easy: 125, medium: 250, hard: 375, deadly: 500 },
        5: { easy: 250, medium: 500, hard: 750, deadly: 1100 },
        6: { easy: 300, medium: 600, hard: 900, deadly: 1400 },
        7: { easy: 350, medium: 750, hard: 1100, deadly: 1700 },
        8: { easy: 450, medium: 900, hard: 1400, deadly: 2100 },
        9: { easy: 550, medium: 1100, hard: 1600, deadly: 2400 },
        10: { easy: 600, medium: 1200, hard: 1900, deadly: 2800 },
        15: { easy: 1100, medium: 2200, hard: 3300, deadly: 5500 },
        20: { easy: 2000, medium: 3900, hard: 5900, deadly: 9500 }
    };

    const baseXp = xpByLevel[Math.min(partyLevel, 20)] || xpByLevel[20];
    const multiplier = partySize / 4;

    return {
        easy: Math.floor(baseXp.easy * multiplier),
        medium: Math.floor(baseXp.medium * multiplier),
        hard: Math.floor(baseXp.hard * multiplier),
        deadly: Math.floor(baseXp.deadly * multiplier)
    };
}

// Get best CR match for XP budget
function getCRForBudget(xpBudget) {
    let bestCR = 0;
    let bestDiff = xpBudget;
    
    for (const [cr, xp] of Object.entries(CR_XP_VALUES)) {
        const diff = Math.abs(xp - xpBudget);
        if (diff < bestDiff) {
            bestDiff = diff;
            bestCR = cr;
        }
    }
    
    return parseFloat(bestCR);
}

// Select random difficulty with weights
function selectRandomDifficulty() {
    const difficulties = ["easy", "medium", "hard", "deadly"];
    const weights = [3, 5, 4, 2];
    const random = Math.random() * weights.reduce((a, b) => a + b);
    
    let sum = 0;
    for (let i = 0; i < difficulties.length; i++) {
        sum += weights[i];
        if (random <= sum) return difficulties[i];
    }
    return "medium";
}

function formatDifficulty(difficulty) {
    const labels = {
        easy: "Easy",
        medium: "Medium",
        hard: "Hard",
        deadly: "Deadly"
    };
    return labels[difficulty] || difficulty;
}

async function selectCreaturesForEncounter(guildKey, targetXP, partyLevel, difficulty) {
    const creatures = await loadCreatures();
    if (!creatures) return [];

    const crMultiplier = {
        "easy": 0.5,
        "medium": 1,
        "hard": 1.5,
        "deadly": 2
    }[difficulty] || 1;
    
    const baseTargetCR = partyLevel * crMultiplier;
    const crVariance = 2 + (partyLevel / 5);
    let minCR = Math.max(0, baseTargetCR - crVariance);
    let maxCR = baseTargetCR + crVariance;
    
    let availableCreatures = filterCreaturesByGuildAndCR(creatures, guildKey, minCR, maxCR);
    
    if (availableCreatures.length === 0) {
        availableCreatures = filterCreaturesByGuildAndCR(creatures, guildKey, 0, 30);
    }
    if (availableCreatures.length === 0) {
        const allGuilds = Object.keys(ENVIRONMENTS).filter(k => k !== 'random');
        for (const guild of allGuilds) {
            availableCreatures = filterCreaturesByGuildAndCR(creatures, guild, minCR, maxCR);
            if (availableCreatures.length > 0) break;
        }
    }
    
    const selected = [];
    let totalXP = 0;
    const shuffled = availableCreatures.sort(() => Math.random() - 0.5);
    
    for (const creature of shuffled) {
        if (totalXP + creature.xp <= targetXP * 1.5) {
            selected.push(creature);
            totalXP += creature.xp;
        }
        if (selected.length >= 4) break;
    }
    
    return selected.length > 0 ? selected : shuffled.slice(0, Math.min(2, shuffled.length));
}

async function generateEncounter() {
    const envSelect = document.getElementById("environment");
    const partySize = parseInt(document.getElementById("partySize").value) || 4;
    const partyLevel = parseInt(document.getElementById("partyLevel").value) || 1;
    const difficultySelect = document.getElementById("difficulty").value;

    if (!envSelect.value || envSelect.value === "") {
        alert("Please select an environment!");
        return;
    }

    let environmentKey = envSelect.value;
    if (environmentKey === "random") {
        const keys = Object.keys(ENVIRONMENTS);
        environmentKey = keys[Math.floor(Math.random() * keys.length)];
    }

    const environment = ENVIRONMENTS[environmentKey];
    let difficulty = difficultySelect;
    if (difficulty === "random") {
        difficulty = selectRandomDifficulty();
    }

    const thresholds = calculateThresholds(partyLevel, partySize);
    const targetXP = thresholds[difficulty];
    
    // Seleciona criaturas para o encontro
    const encounterCreatures = await selectCreaturesForEncounter(
        environmentKey, targetXP, partyLevel, difficulty
    );
    
    const totalXP = encounterCreatures.reduce((sum, c) => sum + c.xp, 0);
    const adjustedXP = totalXP * (partySize / 4);

    const creaturesHTML = encounterCreatures.map((c, i) => {
        const artUrl = c.data.image_uris?.art_crop || '';
        const thumbStyle = artUrl
            ? `background-image:url(${artUrl});background-size:cover;background-position:center;`
            : 'background:#2d3561;';
        return `
        <div class="encounter-card" onclick="toggleStatBlock(this, ${i})">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:48px;height:48px;border-radius:4px;flex-shrink:0;${thumbStyle}"></div>
                <div>
                    <strong>${c.name}</strong>
                    <div style="font-size:0.85em;color:#aaa;margin-top:2px;">CR ${c.cr} &bull; ${c.xp} XP &bull; ${c.data.meta || ''}</div>
                </div>
                <span style="margin-left:auto;color:#667eea;font-size:1.1em;">&#9660;</span>
            </div>
            <div class="statblock-expand" style="display:none;margin-top:10px;"></div>
        </div>`;
    }).join('');

    let html = `
        <div class="environment-info">
            <strong>${environment.icon} ${environment.name}</strong>
            <p><em>${environment.description}</em></p>
        </div>

        <div style="background:rgba(102,126,234,0.15);border-radius:4px;padding:15px;margin:15px 0;border-left:4px solid #667eea;">
            <strong style="color:#667eea;font-size:1.1em;">Encounter Creatures</strong>
            <div class="encounters-grid" style="margin-top:10px;">${creaturesHTML}</div>
        </div>

        <div style="background:rgba(0,0,0,0.3);border-radius:4px;padding:15px;margin:15px 0;border-left:3px solid #764ba2;">
            <strong style="color:#764ba2;">Statistics</strong>
            <p style="margin:10px 0 0 0;color:#aaa;">
                Raw XP: ${totalXP} &bull; Adjusted (${partySize} PCs): ${adjustedXP.toFixed(0)}<br>
                Threshold ${difficulty.toUpperCase()}: ${targetXP} XP<br>
                Threat: <em>${environment.threat}</em>
            </p>
        </div>

        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:15px;align-items:center;">
            <span class="difficulty-indicator difficulty-${difficulty}">${formatDifficulty(difficulty)}</span>
            <span style="color:#aaa;">${partySize} players &bull; Level ${partyLevel}</span>
        </div>

        <div style="margin-top:20px;">
            <button onclick="openCreaturesTab()" style="background:#667eea;color:white;border:none;padding:10px 20px;border-radius:4px;cursor:pointer;font-weight:600;">
                View All Creatures
            </button>
        </div>
    `;

    _encounterCreaturesData = encounterCreatures;

    // Atualiza UI
    document.getElementById("encounterTitle").textContent = `Encounter in ${environment.name}`;
    document.getElementById("encounterContent").innerHTML = html;
    document.getElementById("encounterResult").classList.add("visible");

    // Scroll para resultado
    setTimeout(() => {
        document.getElementById("encounterResult").scrollIntoView({ behavior: "smooth" });
    }, 100);
}

function openCreaturesTab() {
    window.location.href = "../index.html";
}

function toggleStatBlock(card, idx) {
    const expand = card.querySelector('.statblock-expand');
    const arrow = card.querySelector('span[style*="margin-left"]');
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
        if (arrow) arrow.innerHTML = '&#9650;';
    } else {
        expand.style.display = 'none';
        if (arrow) arrow.innerHTML = '&#9660;';
    }
}

document.addEventListener("keypress", e => {
    if (e.key === "Enter") generateEncounter();
});

window.addEventListener('load', () => {
    loadCreatures().then(data => {
        if (data) console.log(`${Object.keys(data).length} creatures loaded`);
    });
});
