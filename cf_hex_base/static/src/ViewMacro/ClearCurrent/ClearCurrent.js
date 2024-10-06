/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class ClearCurrent extends Component {
    static template = "ClearCurrent"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
    }

    resetCurrentSelect(){
        this.store.resetCurrentSelect()
    }
}
