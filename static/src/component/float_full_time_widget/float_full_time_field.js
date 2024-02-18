/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { parseFloatTime } from "@web/views/fields/parsers";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useNumpadDecimal } from "@web/views/fields/numpad_decimal_hook";

import { Component } from "@odoo/owl";

export class FloatFullTime extends Component {
    // PROPS AGGIUNTIVE - OPTIONS WIDGET
    static defaultProps = {
        props_extra_1: false,
        props_extra_2: false,
        props_extra_3: 'readonly',
    };
    setup() {
        useInputField({
            getValue: () => this.formattedValue,
            refName: "numpadDecimal",
            parse: (v) => parseFloatTime(v),
        });
        useNumpadDecimal();
    }

    get formattedValue() {
        var value = this.props.value;
        var props_extra_1 = this.props.props_extra_1;
        var props_extra_2 = this.props.props_extra_2;
        var props_extra_3 = this.props.props_extra_3;

        this.props.props_extra_3 = 'readonly';
        return 'value' + value + '!';
    }
}

FloatFullTime.template = "web.FloatFullTime";
FloatFullTime.props = {
    ...standardFieldProps,
    inputType: { type: String, optional: true },
    placeholder: { type: String, optional: true },
    // PROPS AGGIUNTIVE - OPTIONS WIDGET
    props_extra_1: { type: Boolean, optional: true },
    props_extra_2: { type: Boolean, optional: true },
    props_extra_3: { type: String, optional: true },
};
FloatFullTime.defaultProps = {
    inputType: "text",
};

FloatFullTime.displayName = _lt("Time");
FloatFullTime.supportedTypes = ["float"];

FloatFullTime.isEmpty = () => false;
FloatFullTime.extractProps = ({ attrs }) => {
    return {
        inputType: attrs.options.type,
        placeholder: attrs.placeholder,
        // PROPS AGGIUNTIVE - OPTIONS WIDGET
        props_extra_1: attrs.options.props_extra_1,
        props_extra_2: attrs.options.props_extra_2,
        props_extra_3: attrs.options.props_extra_3,
    };
};

registry.category("fields").add("float_full_time", FloatFullTime);
