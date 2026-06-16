import {createCustomElement} from './helpers/create-custom-element.js';

const HTML = `<style>
  ::slotted(h1) {
    font-family: 'Libre Baskerville', 'Lora', Georgia, serif;
    color: #7A200D;
    font-weight: 700;
    margin: 0;
    font-size: 23px;
    letter-spacing: 1px;
    font-variant: small-caps;
  }
  ::slotted(h2) {
    font-weight: normal;
    font-style: italic;
    font-size: 12px;
    margin: 0;
  }
</style>
<slot></slot>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('creature-heading', contentNode);
