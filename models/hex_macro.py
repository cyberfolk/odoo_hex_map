# -*- coding: utf-8 -*-
from odoo import fields, models, api
from ..utility.costant import BORDERS_MAP
from ..utility.odoo_to_json import obj_odoo_to_json


class MacroArea(models.Model):
    _name = "hex.macro"
    _inherit = ['hex.mixin']
    _description = "Macro-Area, contains Quadrants."

    quad_ids = fields.One2many(
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

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            record.code = (chr(ord('A') + record.index - 1))

    def set_quads_borders(self):
        """Metodo per impostare i bordi dei quadranti. Gestita la casistica dei lati dei quadranti del secondo cerchio
         che non confinano con nulla. Il border che non confina con nulla rimane settato a nulla"""
        quad_void = self.env.ref('cf_hex_map.hex_quad_void')
        index_to_quad = {x.index: x for x in self.quad_ids}  # Crea un dizionario per mappare gli index agli esagoni
        for quad in self.quad_ids:
            borders = BORDERS_MAP[quad.index]
            quad.border_N = index_to_quad.get(borders[0]) or quad_void
            quad.border_NE = index_to_quad.get(borders[1]) or quad_void
            quad.border_SE = index_to_quad.get(borders[2]) or quad_void
            quad.border_S = index_to_quad.get(borders[3]) or quad_void
            quad.border_SW = index_to_quad.get(borders[4]) or quad_void
            quad.border_NW = index_to_quad.get(borders[5]) or quad_void
