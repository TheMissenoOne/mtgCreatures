import {createCustomElement} from './helpers/create-custom-element.js';

const HTML = `<style>
  .bar {
    height: 5px;
    background: #E69A28;
    border: 1px solid #000;
    position: relative;
    z-index: 1;
    max-width: 100%;
  }
  :host { display: inline-block; max-width: 100%; color: #1a1a1a; }
  #content-wrap {
    font-family: 'Noto Sans', Calibri, Helvetica, Arial, sans-serif;
    font-size: 13.5px;
    background: #FDF1DC;
    padding: 0.6em;
    padding-bottom: 0.5em;
    border: 1px #DDD solid;
    box-shadow: 0 0 1.5em #867453;
    position: relative;
    z-index: 0;
    margin-left: 2px;
    margin-right: 2px;
    -webkit-columns: 400px;
       -moz-columns: 400px;
            columns: 400px;
    -webkit-column-gap: 40px;
       -moz-column-gap: 40px;
            column-gap: 40px;
    -webkit-column-fill: auto;
       -moz-column-fill: auto;
            column-fill: auto;
  }
  :host([data-two-column]) #content-wrap {
    max-width: 860px;
  }
  ::slotted(h3) {
    border-bottom: 1px solid #7A200D;
    color: #7A200D;
    font-size: 21px;
    font-variant: small-caps;
    font-weight: normal;
    letter-spacing: 1px;
    margin: 0;
    margin-bottom: 0.3em;
    break-inside: avoid-column;
    break-after: avoid-column;
  }
  ::slotted(p) { margin-top: 0.3em; margin-bottom: 0.9em; line-height: 1.5; }
  ::slotted(*:last-child) { margin-bottom: 0; }
</style>
<div class="bar"></div>
<div id="content-wrap"><slot></slot></div>
<div class="bar"></div>`;

const contentNode = document.createRange().createContextualFragment(HTML);
createCustomElement('stat-block', contentNode);
