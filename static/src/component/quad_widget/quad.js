/** @odoo-module **/

const { xml, Component } = owl;
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class QuadField extends Component {
    setup() {
        super.setup();
    }

    static POSITION = {
        "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75],
        "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30]
    };

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

QuadField.template = "quad_template";
QuadField.props = { ...standardFieldProps, };
registry.category("fields").add("quad", QuadField);
