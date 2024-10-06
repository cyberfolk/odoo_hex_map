/** @odoo-module **/
import { xml, Component, onWillStart, useState, onWillUpdateProps} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { getAxes } from '../utility/utils.js';
const fieldRegistry = registry.category("fields");

export class QuadField extends Component {
    static components = { };
    static template = "quad_template";

    setup() {
        super.setup();
        this.orm = useService("orm");
        let quad_id = this.props.record.resId

        onWillStart(async () => {
            this.quad = await this.get_json_quad(quad_id)
            this.external_hexs = await this.get_json_external_hexs(quad_id)
        });

        onWillUpdateProps(async (nextProps) => {
            let quad_id = nextProps.record.resId
            this.quad = await this.get_json_quad(quad_id)
            this.external_hexs = await this.get_json_external_hexs(quad_id)
        });
    }

    get_json_quad(quad_id){
        const quad = this.orm.call("hex.quad", "get_json_quad", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return quad
    }

    get_json_external_hexs(quad_id){
        const external_hexs = this.orm.call("hex.quad", "get_json_external_hexs", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return external_hexs
    }

    getHexStyle(hex) {
        return `${getAxes(hex.index)}; background-color: ${hex.color}; filter: brightness(${100 - (1 + hex.circle_order) * hex.circle_number}%);`
    }

    getHexMissingStyle(hex) {
        let index = hex.index + 6 ;
        index = index > 19 ? (hex.index - 6) : index;
        return `${getAxes(index)}; background-color: #eeeeee;`
    }

    getMissingHexStyle(index) {
        return `${getAxes(index)}; background-color: #eeeeee;`
    }
}

export const quadField = {
    component: QuadField,
};

fieldRegistry.add("quad", quadField);
