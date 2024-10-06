/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class CurrentZoom extends Component {
    static template = "CurrentZoom"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            zoom: '100%',
        })
    }

    setZoom(percentage){
        this.store.zoom = percentage
    }
}
