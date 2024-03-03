# -*- coding: utf-8 -*-
from odoo import fields, models, api
from ..utility.odoo_to_json import obj_odoo_to_json


class MacroArea(models.Model):
    _name = "hex.macro"
    _inherit = ['hex.mixin']
    _description = "Macro-Area, contains Quadrants."

    quadrant_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='macro_id',
    )

    tmp = fields.Char(
        string="tmp",
        help="Usato temporaneamente per agganciare il widget"
    )

    @api.model
    def get_json_macro(self):
        """Metodo richiamato dal orm di macro.js
            :return: Json della Macro-Area."""
        self_macro = self.env['hex.macro'].browse(1)
        json_macro = obj_odoo_to_json(self_macro)
        return json_macro
