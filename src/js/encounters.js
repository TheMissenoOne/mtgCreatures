// Ravnica Encounter Generator - Enhanced with Real Creatures
// Carrega criaturas de final.json

let CREATURES_DATABASE = null;

// Dados de ambientes e encontros temáticos
const ENVIRONMENTS = {
    azorius: {
        name: "Distrito Administrativo Azorius",
        icon: "🏛️",
        description: "Complexos governamentais, tribunais, arquivos infinitos.",
        guilds: ["Azorius"],
        guildColors: [["W", "U"]],
        threat: "Auditoria, prisão ou confisco de bens.",
    },
    orzhov: {
        name: "Catedral Orzhov",
        icon: "⛪",
        description: "Basílicas luxuosas que são bancos, igrejas e cofres.",
        guilds: ["Orzhov"],
        guildColors: [["W", "B"]],
        threat: "Cobrança de dívidas, contratos vinculativos.",
    },
    izzet: {
        name: "Laboratório Izzet",
        icon: "🧪",
        description: "Torres experimentais instáveis e perigosas.",
        guilds: ["Izzet"],
        guildColors: [["U", "R"]],
        threat: "Experimentos fora de controle desastrosamente.",
    },
    rakdos: {
        name: "Arena Rakdos",
        icon: "🎭",
        description: "Teatro, circo, massacre ritual.",
        guilds: ["Rakdos"],
        guildColors: [["B", "R"]],
        threat: "Caos, performance sádica, derramamento de sangue.",
    },
    selesnya: {
        name: "Jardim Selesnya",
        icon: "🌳",
        description: "Oásis vivos dentro da cidade.",
        guilds: ["Selesnya"],
        guildColors: [["G", "W"]],
        threat: "Incorporação forçada, ritual de comunhão.",
    },
    golgari: {
        name: "Subterrâneos Golgari",
        icon: "☠️",
        description: "Necrópoles, fungos, ecossistema morto-vivo.",
        guilds: ["Golgari"],
        guildColors: [["B", "G"]],
        threat: "Enxame necrofágico, os mortos-vivos despertam.",
    },
    simic: {
        name: "Zonas Simic",
        icon: "🧬",
        description: "Reservas biológicas e câmaras de mutação.",
        guilds: ["Simic"],
        guildColors: [["U", "G"]],
        threat: "Híbridos instáveis e evolução acelerada.",
    },
    gruul: {
        name: "Territorium Gruul",
        icon: "🪨",
        description: "Florestas destruídas, ruínas antigas, selvageria.",
        guilds: ["Gruul"],
        guildColors: [["G", "R"]],
        threat: "Fúria bruta, besta selvagem, destruição.",
    },
    boros: {
        name: "Quartel Boros",
        icon: "⚔️",
        description: "Fortalezas militares, posto de comando.",
        guilds: ["Boros"],
        guildColors: [["R", "W"]],
        threat: "Aplicação brutal da lei marcial.",
    },
    dimir: {
        name: "Célula Dimir",
        icon: "🕵️",
        description: "Espaços ocultos, bibliotecas proibidas.",
        guilds: ["Dimir"],
        guildColors: [["U", "B"]],
        threat: "Infiltração, assassinato secreto, memórias roubadas.",
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

// Helper: generate HTML stat block (identical to index's getStatBlock)
// reused here so encounters can show full creature statblocks.
const getStatBlock = (data) => {
    if (!data || typeof data !== 'object') {
        return '<p style="color: red;">Invalid creature data</p>';
    }

    const name = data.name || 'Unknown Creature';
    const meta = data.meta || '';
    const artUrl = data.image_uris?.art_crop || 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%22 height=%22100%22%3E%3Crect fill=%22%23ddd%22 width=%22100%22 height=%22100%22/%3E%3C/svg%3E';
    const ac = data['Armor Class'] ?? '10';
    const hp = data['Hit Points'] ?? '10';
    const speed = data['Speed'] || '30 ft.';
    const str = data.STR ?? '10';
    const dex = data.DEX ?? '10';
    const con = data.CON ?? '10';
    const int = data.INT ?? '10';
    const wis = data.WIS ?? '10';
    const cha = data.CHA ?? '10';
    const senses = data.Senses || 'Passive Perception 10';
    const languages = data.Languages || '—';
    const skills = data.Skills || '—';
    const challenge = data.Challenge || '0 (0 XP)';
    const traits = data.Traits || '';
    const actions = data.Actions || '<p><em>No actions listed</em></p>';
    const damageImmunities = data['Damage Immunities'] || '';
    const damageResistances = data['Damage Resistances'] || '';
    const conditionImmunities = data['Condition Immunities'] || '';

    let immunityBlocks = '';
    if (damageImmunities) {
        immunityBlocks += `<property-line><h4>Damage Immunities</h4><p>${damageImmunities}</p></property-line>`;
    }
    if (damageResistances) {
        immunityBlocks += `<property-line><h4>Damage Resistances</h4><p>${damageResistances}</p></property-line>`;
    }
    if (conditionImmunities) {
        immunityBlocks += `<property-line><h4>Condition Immunities</h4><p>${conditionImmunities}</p></property-line>`;
    }

    return `<div class="card_art" style="background-image: url(${artUrl})"><stat-block id="stat-block">
    <creature-heading>
      <h1>${name}</h1>
      <h2>${meta}</h2>
    </creature-heading>

    <top-stats>
      <property-line>
        <h4>Armor Class</h4>
        <p>${ac}</p>
      </property-line>
      <property-line>
        <h4>Hit Points</h4>
        <p>${hp}</p>
      </property-line>
      <property-line>
        <h4>Speed</h4>
        <p>${speed}</p>
      </property-line>

      <abilities-block data-str="${str}"
                       data-dex="${dex}"
                       data-con="${con}"
                       data-int="${int}"
                       data-wis="${wis}"
                       data-cha="${cha}"></abilities-block>

      ${immunityBlocks}
      <property-line>
        <h4>Senses</h4>
        <p>${senses}</p>
      </property-line>
      <property-line>
        <h4>Languages</h4>
        <p>${languages}</p>
      </property-line>
      <property-line>
        <h4>Skills</h4>
        <p>${skills}</p>
      </property-line>
      <property-line>
        <h4>Challenge</h4>
        <p>${challenge}</p>
      </property-line>
    </top-stats>

    ${traits}
    <h3>Actions</h3>
    ${actions}
  </stat-block></div>`;
};

// Carrega criaturas de final.json
async function loadCreatures() {
    if (CREATURES_DATABASE) return CREATURES_DATABASE;
    
    try {
        const response = await fetch('./final.json');
        CREATURES_DATABASE = await response.json();
        return CREATURES_DATABASE;
    } catch (error) {
        console.error('Erro carregando creatures:', error);
        return null;
    }
}

// Converte colors array em guild key, ex: ['W', 'U'] => 'azorius'
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

// Extrai CR numérico de string como "8 (3900 XP)"
function parseCR(challengeStr) {
    if (!challengeStr) return 0;
    const match = challengeStr.match(/^([\d/\.]+)/);
    return match ? match[1] : '0';
}

// Filtra criaturas por guilda e intervalo de CR
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
        
        // Exact 2-color match for guild
        const creatureGuild = colorsToGuild(colors);
        if (creatureGuild === guildKey) {
            matches = true;
        }
        
        // 1-color creatures matching guild primary color
        else if (colors.length === 1) {
            const guildColor = guildMono[guildKey];
            if (colors[0] === guildColor) {
                matches = true;
            }
        }
        
        if (matches) {
            const cr = parseFloat(parseCR(creature.Challenge));
            if (cr >= minCR && cr <= maxCR) {
                // include reference to full data so we can render stat block later
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

// Calcula XP thresholds baseado no nível e tamanho do grupo
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

// Calcula CR necessário para o XP budget
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

// Seleciona dificuldade aleatória com pesos
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

// Formata dificuldade com estilo
function formatDifficulty(difficulty) {
    const labels = {
        easy: "Fácil",
        medium: "Médio",
        hard: "Difícil",
        deadly: "Mortal"
    };
    return labels[difficulty] || difficulty;
}

// Seleciona criaturas para construir um encontro
async function selectCreaturesForEncounter(guildKey, targetXP, partyLevel, difficulty) {
    const creatures = await loadCreatures();
    if (!creatures) return [];
    
    // Ajusta intervalo de CR baseado em dificuldade e nível
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
    
    // Se não houver criaturas no intervalo, expandir para toda guilda
    if (availableCreatures.length === 0) {
        availableCreatures = filterCreaturesByGuildAndCR(creatures, guildKey, 0, 30);
    }
    
    // Se ainda sem criaturas, usar qualquer guilda com criaturas
    if (availableCreatures.length === 0) {
        const allGuilds = Object.keys(ENVIRONMENTS).filter(k => k !== 'random');
        for (const guild of allGuilds) {
            availableCreatures = filterCreaturesByGuildAndCR(creatures, guild, minCR, maxCR);
            if (availableCreatures.length > 0) break;
        }
    }
    
    // Seleciona criaturas para atingir o XP target
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

// Gera o encontro
async function generateEncounter() {
    const envSelect = document.getElementById("environment");
    const partySize = parseInt(document.getElementById("partySize").value) || 4;
    const partyLevel = parseInt(document.getElementById("partyLevel").value) || 1;
    const difficultySelect = document.getElementById("difficulty").value;

    if (!envSelect.value || envSelect.value === "") {
        alert("Por favor, selecione um ambiente!");
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

    // Formata lista de criaturas
    const creaturesHTML = encounterCreatures.map(c => `
        <div style="background: rgba(102, 126, 234, 0.1); padding: 12px; margin: 8px 0; border-left: 3px solid #667eea; border-radius: 4px;">
            <strong style="color: #667eea;">⚔️ ${c.name}</strong>
            <div style="font-size: 0.9em; color: #aaa; margin-top: 4px;">
                CR ${c.cr} (${c.xp} XP) • ${c.challenge}
            </div>
        </div>
        <div class="statblock" style="margin-bottom:20px;">
            ${getStatBlock(c.data)}
        </div>
    `).join('');

    // Gera HTML do resultado
    let html = `
        <div class="environment-info">
            <strong>📍 ${environment.icon} ${environment.name}</strong>
            <p><em>${environment.description}</em></p>
        </div>

        <div style="background: rgba(102, 126, 234, 0.15); border-radius: 4px; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea;">
            <strong style="color: #667eea; font-size: 1.1em;">⚔️ Criaturas do Encontro:</strong>
            ${creaturesHTML}
        </div>

        <div style="background: rgba(0, 0, 0, 0.3); border-radius: 4px; padding: 15px; margin: 15px 0; border-left: 3px solid #764ba2;">
            <strong style="color: #764ba2;">📊 Estatísticas:</strong>
            <p style="margin: 10px 0 0 0; color: #aaa;">
                • XP Raw: ${totalXP} | XP Ajustado (${partySize} PCs): ${adjustedXP.toFixed(0)}<br>
                • Threshold ${difficulty.toUpperCase()}: ${targetXP} XP<br>
                • Ameaça: <em>${environment.threat}</em>
            </p>
        </div>

        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 15px; align-items: center;">
            <span class="difficulty-indicator difficulty-${difficulty}">
                ${difficulty.toUpperCase()}: ${formatDifficulty(difficulty)}
            </span>
            <span style="color: #aaa;">
                | 👥 ${partySize} PCs | ⚔️ Nível ${partyLevel}
            </span>
        </div>

        <div style="margin-top: 20px; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 4px;">
            <strong style="color: #667eea;">💡 Dica do Mestre:</strong>
            <p style="margin: 10px 0 0 0;">
                Use as criaturas do encontro e suas traits para criar combates dinâmicos. 
                Acesse o navegador de criaturas para revisar as abilities completas.
            </p>
            <button onclick="openCreaturesTab()" style="
                margin-top: 12px;
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-weight: 600;
            ">📖 Ver Criaturas Completas</button>
        </div>
    `;

    // Atualiza UI
    document.getElementById("encounterTitle").textContent = `⚔️ Encontro em ${environment.name}`;
    document.getElementById("encounterContent").innerHTML = html;
    document.getElementById("encounterResult").classList.add("visible");

    // Scroll para resultado
    setTimeout(() => {
        document.getElementById("encounterResult").scrollIntoView({ behavior: "smooth" });
    }, 100);
}

// Abre aba de criaturas
function openCreaturesTab() {
    window.location.href = "index.html";
}

// Event listeners
document.getElementById("environment").addEventListener("change", function() {
    if (this.value && this.value !== "") {
        const env = ENVIRONMENTS[this.value === "random" ? "azorius" : this.value];
    }
});

// Enter para gerar encontro
document.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        generateEncounter();
    }
});

// Carrega criaturas ao iniciar a página
window.addEventListener('load', () => {
    loadCreatures().then(data => {
        if (data) {
            console.log(`✓ ${Object.keys(data).length} creatures loaded`);
        }
    });
});
