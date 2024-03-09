# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Hex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.mixin']
    _description = "Hexagonal cell"

    quad_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant",
    )

    external_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant Esterno",
    )

    border_N = fields.Many2one(
        comodel_name='hex.hex',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.hex',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.hex',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.hex',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.hex',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.hex',
        string="NW",
        help="Confine Nord-Ovest"
    )

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            if record.id == self.env.ref('cf_hex_map.hex_macro_1').id:
                code = 'void'
            else:
                code = f"{record.quad_id.code}"
                code += f".{str(record.circle_order).zfill(2)}"
                code += f".{str(record.circle_number).zfill(2)}"
            record.code = code

    def tmp_debug(self):
        stop = 0
        self.quad_id.set_external_ids()
