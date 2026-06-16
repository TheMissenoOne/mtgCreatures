import {createCustomElement} from './helpers/create-custom-element.js';

const HTML = `<style>
  svg {
    fill: #922610;
    stroke: #922610;
    margin-top: 0.6em;
    margin-bottom: 0.35em;
  }
</style>
<svg height="5" width="100%">
  <polyline points="0,0 400,2.5 0,5"/>
</svg>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('tapered-rule', contentNode);
