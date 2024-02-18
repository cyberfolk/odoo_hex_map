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

    tmp_str1 = fields.Char(string="tmp_str1", )
    tmp_str2 = fields.Char(string="tmp_str2", )
    tmp_flt = fields.Float(string="tmp_flt", )

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            code = f"{record.quad_id.code}"
            code += f".{str(record.circle_order).zfill(2)}"
            code += f".{str(record.circle_number).zfill(2)}"
            record.code = code
