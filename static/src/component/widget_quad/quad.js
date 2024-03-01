/** @odoo-module **/

import { xml, Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
const fieldRegistry = registry.category("fields");

export class QuadField extends Component {
    static components = { };
    static template = "quad_template";
    static POSITION = {
        "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75],
        "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30]
    };
    static props = {
        ...standardFieldProps,
    };
    setup() {
        super.setup();
        this.orm = useService("orm");

        // TODO-: Sostituire printHelloWorld con una funzione che passi i dati che servono al javascript
        this.orm.call("hex.quad", "printHelloWorld", [], {}).then(
            function (result) {
                console.log(result)
            }
        )
        //this.state = useState({ value: this.props.value, });
    }

    getAxes(index) {
        const REDUCTION = 0.95;
        // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
        // In this way we have the perception that the padding of the QUADRANTS increases
        const asse_y = 50 + QuadField.POSITION.Y[index - 1] * REDUCTION + "%";
        const asse_x = 50 + QuadField.POSITION.X[index - 1] * REDUCTION + "%";
        return `top: ${asse_y}; left: ${asse_x};`
    }

    getHexStyle(hex) {
        return `${this.getAxes(hex.index)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }
}

export const quadField = {
    component: QuadField,
};

fieldRegistry.add("quad", quadField);
