/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { parseFloatTime } from "@web/views/fields/parsers";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useNumpadDecimal } from "@web/views/fields/numpad_decimal_hook";

import { Component } from "@odoo/owl";

export class FloatFullTime extends Component {
    // PROPS AGGIUNTIVE - OPTIONS WIDGET - usate in formattedValue().
    static defaultProps = {
        round_off: false,
        time_only: false,
        mode: 'readonly',
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
       /**
        * Description:
        * -> round_off - true: display template without milliseconds (false by default),
        * -> time_only - true: display template without days (false by default).
        * -> mode - 'edit', 'readonly', e.t.c., if mode === 'edit',
        * days are represented in template in any way,
        * else days are not represented on view (even if time_only !== true).
        */

        var value = this.props.value;
        var round_off = this.props.round_off;
        var time_only = this.props.time_only;
        var mode = this.props.mode;

        var parent_prefix = '';
        var in_value = value;
        if (value < 0) {
            in_value = Math.abs(value);
            parent_prefix = '-';
        }
        var total_sec = Math.floor(in_value);
        var milliseconds = Math.round(in_value % 1 * 1000);
        if (milliseconds === 1000) {
            milliseconds = 0;
            total_sec += 1;
        }

        var minutes = Math.floor(total_sec / 60);
        var seconds = Math.floor(total_sec % 60);

        var hours = Math.floor(minutes / 60);
        minutes = Math.floor(minutes % 60);

        var days = 0;
        if (time_only !== true) {
            days = Math.floor(hours / 24);
            hours = Math.floor(hours % 24);
        }

        var pattern = '%2$02d:%3$02d:%4$02d';
        if (time_only !== true) {
            if (days !== 0 || mode === 'edit') {
                pattern = '%1$01d' + _lt('d') + ' ' + pattern;
            }
        }
        if (round_off !== true) {
            pattern += ',%5$03d';
        }

        pattern = parent_prefix + pattern;

        return _.str.sprintf(
            pattern, days, hours, minutes, seconds, milliseconds);
    }
}

FloatFullTime.template = "web.FloatFullTime";
FloatFullTime.props = {
    ...standardFieldProps,
    inputType: { type: String, optional: true },
    placeholder: { type: String, optional: true },
    // PROPS AGGIUNTIVE - OPTIONS WIDGET - usate in formattedValue().
    round_off: { type: Boolean, optional: true },
    time_only: { type: Boolean, optional: true },
    mode: { type: String, optional: true },
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
        // PROPS AGGIUNTIVE - OPTIONS WIDGET - usate in formattedValue().
        round_off: attrs.options.round_off,
        time_only: attrs.options.time_only,
        mode: attrs.options.mode,
    };
};

registry.category("fields").add("float_full_time", FloatFullTime);
