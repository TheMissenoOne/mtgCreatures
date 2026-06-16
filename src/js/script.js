let ALL_CREATURES = [];
let activeColor = 'all';
let selectedName = null;

const COLOR_CLASS = { W: 'mana-w', U: 'mana-u', B: 'mana-b', R: 'mana-r', G: 'mana-g' };
const COLOR_LABEL = { W: 'W', U: 'U', B: 'B', R: 'R', G: 'G' };

function parseCRNum(challengeStr) {
  if (!challengeStr) return 0;
  const m = challengeStr.match(/^([\d/]+)/);
  if (!m) return 0;
  if (m[1].includes('/')) {
    const [a, b] = m[1].split('/');
    return parseInt(a) / parseInt(b);
  }
  return parseInt(m[1]);
}

function manaSymbols(manaCost) {
  if (!manaCost) return '';
  return manaCost.replace(/\{([^}]+)\}/g, (_, s) => {
    const key = s.toUpperCase();
    const cls = COLOR_CLASS[key] || '';
    return `<span class="mana-symbol ${cls}">${s}</span>`;
  });
}

function renderCreatureList(creatures) {
  const list = document.getElementById('creatureList');
  list.innerHTML = '';
  if (!creatures.length) {
    list.innerHTML = '<div class="no-results">No creatures found</div>';
    return;
  }
  const frag = document.createDocumentFragment();
  for (const c of creatures) {
    const div = document.createElement('div');
    div.className = 'creature-item' + (c.name === selectedName ? ' active' : '');
    div.dataset.name = c.name;

    const dot = document.createElement('span');
    dot.className = `rarity-dot ${c.rarity || 'common'}`;

    const nameEl = document.createElement('span');
    nameEl.className = 'creature-name';
    nameEl.textContent = c.name;

    const crTag = document.createElement('span');
    crTag.className = 'cr-tag';
    const crNum = parseCRNum(c.Challenge);
    crTag.textContent = `CR ${c.Challenge ? c.Challenge.split(' ')[0] : '0'}`;

    div.appendChild(dot);
    div.appendChild(nameEl);
    div.appendChild(crTag);
    div.addEventListener('click', () => selectCreature(c.name));
    frag.appendChild(div);
  }
  list.appendChild(frag);
}

function getFiltered() {
  const search = (document.getElementById('searchInput')?.value || '').toLowerCase();
  const crMin = parseFloat(document.getElementById('crMin')?.value ?? 0);
  const crMax = parseFloat(document.getElementById('crMax')?.value ?? 30);
  const rarity = document.getElementById('rarityFilter')?.value || '';
  const sort = document.getElementById('sortSelect')?.value || 'name';

  let result = ALL_CREATURES.filter(c => {
    if (search && !c.name.toLowerCase().includes(search)) return false;
    const cr = parseCRNum(c.Challenge);
    if (cr < crMin || cr > crMax) return false;
    if (rarity && c.rarity !== rarity) return false;
    if (activeColor !== 'all') {
      const colors = c.colors || [];
      if (!colors.includes(activeColor)) return false;
    }
    return true;
  });

  result.sort((a, b) => {
    if (sort === 'cr') return parseCRNum(a.Challenge) - parseCRNum(b.Challenge);
    if (sort === 'cr-desc') return parseCRNum(b.Challenge) - parseCRNum(a.Challenge);
    if (sort === 'rarity') {
      const order = { common: 0, uncommon: 1, rare: 2, mythic: 3 };
      return (order[a.rarity] ?? 0) - (order[b.rarity] ?? 0);
    }
    return a.name.localeCompare(b.name);
  });

  return result;
}

function applyFilters() {
  const filtered = getFiltered();
  renderCreatureList(filtered);
  const badge = document.getElementById('countBadge');
  if (badge) badge.textContent = `${filtered.length} / ${ALL_CREATURES.length}`;
}

function selectCreature(name) {
  selectedName = name;
  history.pushState({ card: name }, '', `?card=${encodeURIComponent(name)}`);

  // Update active state in list
  document.querySelectorAll('.creature-item').forEach(el => {
    el.classList.toggle('active', el.dataset.name === name);
  });

  const creature = ALL_CREATURES.find(c => c.name === name);
  if (!creature) return;

  document.getElementById('mainContent').innerHTML = renderCreatureDisplay(creature);
}

function renderCreatureDisplay(data) {
  const artUrl = data.image_uris?.art_crop || '';
  const rarity = data.rarity || 'common';
  const name = data.name || 'Unknown';
  const meta = data.meta || '';
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

  const colors = data.colors || [];
  const colorPips = colors.map(c =>
    `<span class="mana-symbol ${COLOR_CLASS[c] || ''}">${COLOR_LABEL[c] || c}</span>`
  ).join('');

  const cmc = data.cmc != null ? data.cmc : '—';
  const pt = (data.power && data.toughness) ? `${data.power}/${data.toughness}` : '—';
  const manaCostHtml = manaSymbols(data.mana_cost || '');

  let immunityBlocks = '';
  if (data['Damage Immunities']) immunityBlocks += `<property-line><h4>Damage Immunities</h4><p>${data['Damage Immunities']}</p></property-line>`;
  if (data['Damage Resistances']) immunityBlocks += `<property-line><h4>Damage Resistances</h4><p>${data['Damage Resistances']}</p></property-line>`;
  if (data['Condition Immunities']) immunityBlocks += `<property-line><h4>Condition Immunities</h4><p>${data['Condition Immunities']}</p></property-line>`;

  const bannerStyle = artUrl ? `background-image: url(${artUrl})` : 'background: #2d3561';

  const flavorBar = data.flavor_text
    ? `<div class="flavor-bar">${data.flavor_text}</div>`
    : '';

  return `<div class="creature-display">
    <div class="card-art-banner" style="${bannerStyle}"></div>
    <div class="mtg-info-bar">
      <span class="rarity-badge ${rarity}">${rarity}</span>
      ${manaCostHtml || colorPips}
      <span class="info-pill">CMC ${cmc}</span>
      <span class="info-pill">P/T ${pt}</span>
    </div>
    <div class="type-line-bar">${data.type_line || ''}</div>

    <stat-block id="stat-block">
      <creature-heading>
        <h1>${name}</h1>
        <h2>${meta}</h2>
      </creature-heading>

      <top-stats>
        <property-line><h4>Armor Class</h4><p>${ac}</p></property-line>
        <property-line><h4>Hit Points</h4><p>${hp}</p></property-line>
        <property-line><h4>Speed</h4><p>${speed}</p></property-line>
        <abilities-block data-str="${str}" data-dex="${dex}" data-con="${con}" data-int="${int}" data-wis="${wis}" data-cha="${cha}"></abilities-block>
        ${immunityBlocks}
        <property-line><h4>Senses</h4><p>${senses}</p></property-line>
        <property-line><h4>Languages</h4><p>${languages}</p></property-line>
        <property-line><h4>Skills</h4><p>${skills}</p></property-line>
        <property-line><h4>Challenge</h4><p>${challenge}</p></property-line>
      </top-stats>

      ${traits}
      <h3>Actions</h3>
      ${actions}
    </stat-block>
    ${flavorBar}
  </div>`;
}

function wireFilters() {
  document.getElementById('searchInput')?.addEventListener('input', applyFilters);
  document.getElementById('crMin')?.addEventListener('input', applyFilters);
  document.getElementById('crMax')?.addEventListener('input', applyFilters);
  document.getElementById('rarityFilter')?.addEventListener('change', applyFilters);
  document.getElementById('sortSelect')?.addEventListener('change', applyFilters);

  document.querySelectorAll('.color-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeColor = btn.dataset.color;
      document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    });
  });
}

window.addEventListener('popstate', e => {
  const name = e.state?.card || new URLSearchParams(location.search).get('card');
  if (name) selectCreature(name);
});

window.onload = () => {
  fetch('data/output/final.json')
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(data => {
      ALL_CREATURES = Object.values(data);
      wireFilters();
      applyFilters();

      const cardName = new URLSearchParams(location.search).get('card');
      if (cardName && data[cardName]) {
        selectCreature(cardName);
      }
    })
    .catch(err => {
      document.getElementById('mainContent').innerHTML =
        `<div class="welcome-msg"><h2 style="color:#c00">Error</h2><p>${err.message}</p></div>`;
      document.getElementById('countBadge').textContent = 'Error';
    });
};
