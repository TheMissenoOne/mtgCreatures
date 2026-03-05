window.onload = function () {
  try {
    const url_string = window.location.href;
    const url = new URL(url_string);
    const cardName = url.searchParams.get("card");
    
    fetch("../../data/output/final.json")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data || Object.keys(data).length === 0) {
          showError("No creature data available. Please run main.py first.");
          return;
        }

        // Setup dropdown
        const dropdownBtn = document.getElementById('dropdownbtn');
        const cardsDiv = document.getElementById('cards');
        
        if (!dropdownBtn || !cardsDiv) {
          showError("UI elements not found.");
          return;
        }

        dropdownBtn.addEventListener('click', myFunction);

        // Populate dropdown with creature names
        const creatureNames = Object.keys(data).sort();
        creatureNames.forEach(name => {
          const link = document.createElement("a");
          link.href = '?card=' + encodeURIComponent(name);
          link.textContent = name;
          cardsDiv.appendChild(link);
        });

        // Display creature if specified in URL
        if (cardName) {
          const creature = data[cardName];
          if (!creature) {
            showError(`Creature "${cardName}" not found. Select one from the dropdown.`);
            return;
          }

          const statBlockHtml = getStatBlock(creature);
          const fichaDiv = document.getElementById("ficha");
          fichaDiv.innerHTML = statBlockHtml;

          // Apply two-column layout if needed
          applyLayout();
        } else {
          showMessage("Select a creature from the dropdown to view its stat block.");
        }
      })
      .catch((error) => {
        console.error("Error loading creature data:", error);
        showError(`Failed to load data: ${error.message}`);
      });
  } catch (err) {
    console.error("Error initializing page:", err);
    showError(`Initialization error: ${err.message}`);
  }
};

/**
 * Apply layout adjustments based on statblock height
 */
function applyLayout() {
  const statBlock = document.getElementById('stat-block');
  if (!statBlock) return;

  const statBlockHeight = statBlock.scrollHeight || statBlock.offsetHeight;
  const viewportHeight = window.innerHeight;
  const threshold = viewportHeight * 2.6;

  if (statBlockHeight >= threshold) {
    statBlock.setAttribute('data-two-column', '');
    statBlock.style = '--data-content-height: calc(100% - 34px);';
  } else {
    statBlock.removeAttribute('data-two-column');
    statBlock.style = '';
  }
}

/**
 * Display error message to user
 */
function showError(message) {
  const fichaDiv = document.getElementById("ficha");
  if (fichaDiv) {
    fichaDiv.innerHTML = `<div style="padding: 20px; color: #c00; background: #fee; border: 1px solid #c00; border-radius: 4px;"><strong>Error:</strong> ${message}</div>`;
  }
  console.error(message);
}

/**
 * Display informational message to user
 */
function showMessage(message) {
  const fichaDiv = document.getElementById("ficha");
  if (fichaDiv) {
    fichaDiv.innerHTML = `<div style="padding: 20px; color: #666; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;">${message}</div>`;
  }
}

/**
 * Generate HTML stat block from creature data
 * @param {Object} data - Creature data object
 * @returns {string} HTML string for stat block
 */
const getStatBlock = (data) => {
  // Validate required data
  if (!data || typeof data !== 'object') {
    return '<p style="color: red;">Invalid creature data</p>';
  }

  // Extract values with fallbacks
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

/**
 * Generate immunity/resistance property blocks
 * @param {Object} data - Creature data with immunity properties
 * @returns {string} HTML property-line elements
 */
const immunities = (data) => {
  let propertyBlocks = '';

  if (data['Damage Immunities']) {
    propertyBlocks += `<property-line><h4>Damage Immunities</h4><p>${data['Damage Immunities']}</p></property-line>`;
  }

  if (data['Damage Resistances']) {
    propertyBlocks += `<property-line><h4>Damage Resistances</h4><p>${data['Damage Resistances']}</p></property-line>`;
  }

  if (data['Condition Immunities']) {
    propertyBlocks += `<property-line><h4>Condition Immunities</h4><p>${data['Condition Immunities']}</p></property-line>`;
  }

  return propertyBlocks;
};

/**
 * Toggle dropdown menu visibility
 */
function myFunction() {
  const cardsDiv = document.getElementById("cards");
  if (cardsDiv) {
    cardsDiv.classList.toggle("show");
  }
}

/**
 * Filter dropdown items based on search input
 */
function filterFunction() {
  const input = document.getElementById("myInput");
  if (!input) return;

  const filter = input.value.toUpperCase();
  const cardsDiv = document.getElementById("cards");
  if (!cardsDiv) return;

  const links = cardsDiv.getElementsByTagName("a");
  for (let i = 0; i < links.length; i++) {
    const textValue = links[i].textContent || links[i].innerText;
    if (textValue.toUpperCase().indexOf(filter) > -1) {
      links[i].style.display = "";
    } else {
      links[i].style.display = "none";
    }
  }
}

/**
 * Close dropdown when clicking outside
 */
document.addEventListener('click', function(event) {
  const cardsDiv = document.getElementById('cards');
  const dropdownBtn = document.getElementById('dropdownbtn');
  
  if (cardsDiv && dropdownBtn && !cardsDiv.contains(event.target) && !dropdownBtn.contains(event.target)) {
    cardsDiv.classList.remove('show');
  }
});function isMobileDevice() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
         window.innerWidth <= 768;
}

window.addEventListener("orientationchange", () => {
  setTimeout(applyLayout, 100);
});

let resizeTimeout;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(applyLayout, 250);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const cards = document.getElementById("cards");
    if (cards?.classList.contains("show")) {
      cards.classList.remove("show");
      document.getElementById("dropdownbtn")?.focus();
    }
  }
});
