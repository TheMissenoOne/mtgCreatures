import {createCustomElement} from './helpers/create-custom-element.js';
import './tapered-rule.js';

const HTML = `<style>
  ::slotted(*) { color: #7A200D; }
</style>
<tapered-rule></tapered-rule>
<slot></slot>
<tapered-rule></tapered-rule>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('top-stats', contentNode);
