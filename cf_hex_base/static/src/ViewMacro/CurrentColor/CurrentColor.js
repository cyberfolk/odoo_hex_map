/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class CurrentColor extends Component {
    static template = "CurrentColor"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            currentColor: "",
        })
    }

    setCurrentColor(color){
        this.store.currentColor = color
    }
}
