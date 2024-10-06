/** @odoo-module **/
import { reactive, useState } from  "@odoo/owl";

export const store = reactive({
    add: add
});


/**
* Aggiunge dinamicamente coppie chiave-valore all'oggetto store.
* @param {Object} item - Oggetto contenente le coppie chiave-valore da aggiungere al store.
*/
function add(item) {
    Object.entries(item).forEach(([key, value]) => {
        this[key] = value;
    });
}

export function useStore() {
    return useState(store);
}
