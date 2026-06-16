import {createCustomElement} from './helpers/create-custom-element.js';

const HTML = `<style>
  :host {
    line-height: 1.4;
    display: block;
    text-indent: -1em;
    padding-left: 1em;
  }
  ::slotted(h4) { margin: 0; display: inline; font-weight: bold; }
  ::slotted(p:first-of-type) { display: inline; text-indent: 0; }
  ::slotted(p) { text-indent: 1em; margin: 0; }
</style>
<slot></slot>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('property-line', contentNode);
