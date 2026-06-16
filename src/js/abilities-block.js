import {createCustomElement} from './helpers/create-custom-element.js';
import './tapered-rule.js';

function abilityModifier(score) {
  return Math.floor((parseInt(score, 10) - 10) / 2);
}

function formattedModifier(mod) {
  return mod >= 0 ? '+' + mod : '–' + Math.abs(mod);
}

function abilityText(score) {
  return `${score} (${formattedModifier(abilityModifier(score))})`;
}

function elementClass(contentNode) {
  return class extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({mode: 'open'}).appendChild(contentNode.cloneNode(true));
    }
    connectedCallback() {
      const root = this.shadowRoot;
      for (const attr of this.attributes) {
        const id = attr.name.split('-')[1];
        const el = root.getElementById(id);
        if (el) el.textContent = abilityText(attr.value);
      }
    }
  };
}

const HTML = `<style>
  table { width: 100%; border: 0; border-collapse: collapse; }
  th, td { width: 50px; text-align: center; }
</style>
<tapered-rule></tapered-rule>
<table>
  <tr><th>STR</th><th>DEX</th><th>CON</th><th>INT</th><th>WIS</th><th>CHA</th></tr>
  <tr>
    <td id="str"></td><td id="dex"></td><td id="con"></td>
    <td id="int"></td><td id="wis"></td><td id="cha"></td>
  </tr>
</table>
<tapered-rule></tapered-rule>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('abilities-block', contentNode, elementClass);
