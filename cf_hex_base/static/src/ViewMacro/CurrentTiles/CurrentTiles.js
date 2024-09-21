/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class CurrentTiles extends Component {
    static template = "CurrentTiles"
    static props = ["*"]

    setup() {
        super.setup();
    }
}
