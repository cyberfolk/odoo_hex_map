/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
const actionRegistry = registry.category("actions");

class ViewMacro extends Component {
    static template = "ViewMacro"
    static components = {};
    static POSITION = {
        "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75],
        "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30]
    };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.macro = null

        onWillStart(async () => {
            this.macro = await this.orm.call("hex.macro", "get_json_macro", [], {})
                .then((result) => {
                    return JSON.parse(result)
                })
            // Rimuovo il quadrante void dalla vista per eliminare errori nel DOM
            this.macro.quadrant_ids = this.macro.quadrant_ids.filter(quad => quad.name !== 'void');
        })
    }

    getAxes(index, REDUCTION) {
        // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
        // In this way we have the perception that the padding of the QUADRANTS increases
        const asse_y = 50 + ViewMacro.POSITION.Y[index - 1] * REDUCTION + "%";
        const asse_x = 50 + ViewMacro.POSITION.X[index - 1] * REDUCTION + "%";
        return `top: ${asse_y}; left: ${asse_x};`
    }

    getHexStyle(hex) {
        return `${this.getAxes(hex.index, 0.95)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }

    getQuadStyle(quad) {
        return `z-index: ${20 - quad.index}; ${this.getAxes(quad.index, 0.97)}; clip-path: ${quad.polygon};`
    }
}

actionRegistry.add('view_macro', ViewMacro);
