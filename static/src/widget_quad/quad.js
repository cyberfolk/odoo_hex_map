/** @odoo-module **/
import { xml, Component, onWillStart, useState, onWillUpdateProps} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
const fieldRegistry = registry.category("fields");

export class QuadField extends Component {
    static components = { };
    static template = "quad_template";
    static POSITION = {
        "X": [0,   0, 18.75, 18.75,  0, -18.75, -18.75,   0, 18.75, 37.5, 37.5, 37.5, 18.75,  0, -18.75, -37.5, -37.5, -37.5, -18.75,0,	18.75,	37.5,	56.25,	56.25,	56.25,	56.25,	37.5,	18.75,	0,	-18.75,	-37.5,	-56.25,	-56.25,	-56.25,	-56.25,	-37.5,	-18.75],
        "Y": [0, -20,   -10,    10, 20,     10,    -10, -40,   -30,  -20,    0,   20,    30, 40,     30,    20,     0,   -20,    -30, -60,	-50,	-40,	-30,	-10,	10,	30,	40,	50,	60,	50,	40,	30,	10,	-10,	-30,	-40,	-50,]
    };
    setup() {
        super.setup();
        this.orm = useService("orm");
        let quad_id = this.props.record.resId

        onWillStart(async () => {
            this.quad = await this.get_json_quad(quad_id)
        });

        onWillUpdateProps(async (nextProps) => {
            let quad_id = nextProps.record.resId
            this.quad = await this.get_json_quad(quad_id)
        });
    }

    get_json_quad(quad_id){
        const quad = this.orm.call("hex.quad", "get_json_quad", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return quad
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
        return `${this.getAxes(hex.index)}; background-color: ${hex.color}; filter: brightness(${100 - (1 + hex.circle_order) * hex.circle_number}%);`
    }

    getOtherHexStyle(num) {
        return `${this.getAxes(num)}; background-color: #eeeeee;`
    }
}

export const quadField = {
    component: QuadField,
};

fieldRegistry.add("quad", quadField);
