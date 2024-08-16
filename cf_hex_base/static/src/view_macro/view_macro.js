/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { getAxes } from '../utility/utils.js';
const actionRegistry = registry.category("actions");

class ViewMacro extends Component {
    static template = "ViewMacro"
    static components = {};

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.macro = null

        onWillStart(async () => {
            this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
        })
    }

    getHexStyle(hex) {
        return `${getAxes(hex.index, 0.95)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }

    getQuadStyle(quad) {
        return `${getAxes(quad.index, 0.97)}; z-index: ${20 - quad.index}; clip-path: ${quad.polygon};`
    }
}

actionRegistry.add('view_macro', ViewMacro);
