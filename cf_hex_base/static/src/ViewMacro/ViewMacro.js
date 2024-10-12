/** @odoo-module **/
import { ClearCurrent } from '@cf_hex_base/ViewMacro/ClearCurrent/ClearCurrent';
import { CurrentColor } from '@cf_hex_base/ViewMacro/CurrentColor/CurrentColor';
import { CurrentTiles } from '@cf_hex_base/ViewMacro/CurrentTiles/CurrentTiles';
import { CurrentZoom } from '@cf_hex_base/ViewMacro/CurrentZoom/CurrentZoom';
import { HexHex } from '@cf_hex_base/ViewMacro/HexHex/HexHex';
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { getAxes } from '../utility/utils.js';
import { store, useStore } from "../store";
const actionRegistry = registry.category("actions");

class ViewMacro extends Component {
    static template = "ViewMacro"
    static props = ["*"]
    static components = { CurrentColor, CurrentZoom, CurrentTiles, ClearCurrent, HexHex };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            macro: null,
        })
        this.store = useStore()

        onWillStart(async () => {
            this.state.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
                .then((result) => { return JSON.parse(result) })
        })
    }

    getQuadStyle(quad) {
        return `${getAxes(quad.index, 0.97)}; z-index: ${20 - quad.index}; clip-path: ${quad.polygon};`
    }

    resetCurrentSelect_ClickOutside(event) {
        if (!event.target.closest('.hex')) {  // Check elemento cliccato non appartenga alla macro_form o ai suoi figli
            this.store.resetCurrentSelect();
        }
    }
}

actionRegistry.add('ViewMacro', ViewMacro);
