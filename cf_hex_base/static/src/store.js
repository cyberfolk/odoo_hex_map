/** @odoo-module **/
import { reactive, useState } from  "@odoo/owl";

export const store = reactive({

    /**
    * Aggiunge dinamicamente coppie chiave-valore all'oggetto store.
    * @param {Object} item - Oggetto contenente le coppie chiave-valore da aggiungere al store.
    */
    add(item) {
        Object.entries(item).forEach(([key, value]) => {
            this[key] = value;
        });
    },

    resetCurrentSelect(){
        this.currentTile.tile_id = ''
        this.currentColor = ''
    },

    isCurrentSelectEmpty(){
        return (!this.currentTile.tile_id && !this.currentColor)
    }

});

export function useStore() {
    return useState(store);
}
