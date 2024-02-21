/** @odoo-module **/

const { xml, Component } = owl;
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class QuadField extends Component {
    // Sovrascrivo il metodo setup(). Metodo fondamentale per gestire la logica del ciclo di vita dei componenti OWL.
    setup() {
        super.setup(); // Richiamo il metodo setup della classe padre per eseguire correttamente l'override.
        console.log(this.props.data)
    }
}

QuadField.template = "quad_template";
// QuadField.defaultProps = { bgColor: "primary", };
QuadField.props = { ...standardFieldProps, };
// QuadField.extractProps = ({ attrs, field }) => { return { bgColor: attrs.options.bg_color, };};

registry.category("fields").add("quad", QuadField);
