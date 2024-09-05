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
        this.zoom = '100%'
        this.currentColor = ""

        onWillStart(async () => {
            this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
        })
    }
    setZoom(percentage){
        this.zoom = percentage
        this.render();
    }

    setCurrentColor(color){
        this.currentColor = color
        this.render();
    }

    /**
     * Cambia il colore di hex con this.currentColor, e poi aggiorna this.macro.
     * Se currentColor non è impostato => non fa nulla
     */
    async changeHexColor(hex){
        const hex_id = hex.id;
        if (!this.currentColor)
            return false

        await this.orm.call("hex.hex", "change_hex_color", [hex_id, this.currentColor], {});
        console.log("Color changed successfully");

        this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
            .then((result) => { return JSON.parse(result) })
        this.render(true);
    }


    getHexStyle(hex) {
        return `${getAxes(hex.index, 0.95)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }

    getQuadStyle(quad) {
        return `${getAxes(quad.index, 0.97)}; z-index: ${20 - quad.index}; clip-path: ${quad.polygon};`
    }
}

actionRegistry.add('view_macro', ViewMacro);
