/** @odoo-module **/

const { xml, Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

export class MacroField extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.orm = useService('orm');
        this.wip_orm_search_read();
        const stato = useState({
          dati: null,
        });

//        console.log(this.props.record.data.quadrant_ids.records)
//        console.log(this.props.record.data.quadrant_ids.records[0].data.hex_ids.records)
//        console.log(this.props.record.data.quadrant_ids.records[0].data.hex_ids.records[0].data)
        super.setup();
    }

    wip_orm_search_read() {
        this.orm.call("hex.macro", "search_read", [], {}).then(
            function (result){
                console.log(result)
            }
        );
    };

    static POSITION = {
        "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75],
        "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30]
    };

    getAxes(index) {
        const REDUCTION = 0.95;
        // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
        // In this way we have the perception that the padding of the QUADRANTS increases
        const asse_y = 50 + MacroField.POSITION.Y[index - 1] * REDUCTION + "%";
        const asse_x = 50 + MacroField.POSITION.X[index - 1] * REDUCTION + "%";
        return `top: ${asse_y}; left: ${asse_x}`
    }

    getHexStyle(hex) {
        return `${this.getAxes(hex.index)}; background-color: ${hex.color}; filter: brightness(${120 - 3 * hex.index}%);`
    }

    getQuadStyle(quad) {
        return `z-index: ${20 - quad.index}; ${this.getAxes(quad.index)}; clip-path: ${quad.polygon};`
    }
}

MacroField.template = "macro_template";
MacroField.props = { ...standardFieldProps, };
registry.category("fields").add("macro", MacroField);
