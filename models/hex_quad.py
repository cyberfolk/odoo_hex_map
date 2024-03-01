# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Quadrant(models.Model):
    _name = "hex.quad"
    _inherit = ['hex.mixin']
    _description = "Quadrant, contains Hexagons."

    macro_id = fields.Many2one(
        comodel_name='hex.macro',
        string="Macro Area",
    )

    hex_list = fields.Char(
        string="Hex list",
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='quad_id',
    )

    polygon = fields.Char(
        string='Polygon'
    )

    tmp = fields.Char(
        string="tmp",
        help="Usato temporaneamente per agganciare il widget"
    )

    @api.model
    def printHelloWorld(self):
        return "AGGIUNGERE QUI I DATI DA PASSARE ALLA RPC"

    @api.model_create_multi
    def create(self, vals):
        quads = super(Quadrant, self).create(vals)
        hex_list = eval(vals[0]['hex_list'])
        hex_macro = self.env.ref('cf_hex_map.hex_macro_1')
        for quad in quads:
            quad.check_name()
            quad.macro_id = self.env.ref('cf_hex_map.hex_macro_1')
            for index in hex_list:
                hex_id = self.env['hex.hex'].create({
                    'quad_id': quad.id,
                    'index': index,
                    'color': quad.color,
                })
                hex_id.check_name()
                quad.hex_ids = [(4, hex_id.id)]
            hex_macro.quadrant_ids = [(4, quad.id)]
        return quads
