# -*- coding: utf-8 -*-
from odoo import fields, models, api
from ..utility.costant import BORDERS_MAP
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

    def set_quads_borders(self):
        """Metodo per impostare i bordi dei quadranti. Gestita la casistica dei lati dei quadranti del secondo cerchio
         che non confinano con nulla. Il border che non confina con nulla rimane settato a nulla"""
        quad_void = self.env.ref('cf_hex_map.hex_quad_void')
        for quad in self.quadrant_ids:
            borders = BORDERS_MAP[quad.index]
            quad.border_N = quad.search([('index', '=', [borders[0]])]) or quad_void
            quad.border_NE = quad.search([('index', '=', [borders[1]])]) or quad_void
            quad.border_SE = quad.search([('index', '=', [borders[2]])]) or quad_void
            quad.border_S = quad.search([('index', '=', [borders[3]])]) or quad_void
            quad.border_SW = quad.search([('index', '=', [borders[4]])]) or quad_void
            quad.border_NW = quad.search([('index', '=', [borders[5]])]) or quad_void
