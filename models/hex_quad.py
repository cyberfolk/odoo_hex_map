# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ..utility.odoo_to_json import obj_odoo_to_json
from ..utility.costant import BORDERS_MAP
from ..utility.costant import EXTERNAL_BORDERS_MAP


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

    external_ids = fields.One2many(
        comodel_name='hex.hex',
        string="External Hexes",
        inverse_name='external_id',
    )

    polygon = fields.Char(
        string='Polygon'
    )

    hook_widget = fields.Char(
        string="hook_widget",
        help="Usato solamente per agganciare il widget del quadrante."
    )

    border_N = fields.Many2one(
        comodel_name='hex.quad',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.quad',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.quad',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.quad',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.quad',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.quad',
        string="NW",
        help="Confine Nord-Ovest"
    )

    @api.model
    def get_json_quad(self, quad_id):
        """Metodo richiamato dal orm di quad.js
            :param quad_id: Id quadrante.
            :return: Json del quadrante."""
        self_quad = self.env['hex.quad'].browse(quad_id)[0]
        json_quad = obj_odoo_to_json(self_quad)
        return json_quad

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

    def set_hexs_borders(self):
        """Metodo per impostare i bordi degli Esagoni. Lascia a None i bordi degli esagoni esterni."""
        for hex in self.hex_ids:
            borders = BORDERS_MAP[hex.index]
            hex.border_N = next((x for x in self.hex_ids if x['index'] == borders[0]), None)
            hex.border_NE = next((x for x in self.hex_ids if x['index'] == borders[1]), None)
            hex.border_SE = next((x for x in self.hex_ids if x['index'] == borders[2]), None)
            hex.border_S = next((x for x in self.hex_ids if x['index'] == borders[3]), None)
            hex.border_SW = next((x for x in self.hex_ids if x['index'] == borders[4]), None)
            hex.border_NW = next((x for x in self.hex_ids if x['index'] == borders[5]), None)

    def set_hexs_external_borders(self):
        """Metodo per impostare i bordi degli Esagoni esterni."""
        filtered_hex_ids = self.hex_ids.filtered(lambda r: r.index != 1)
        for hex in filtered_hex_ids:
            hex_external_borders = EXTERNAL_BORDERS_MAP[hex.index]
            for border_key, border_value in hex_external_borders.items():
                quad_border_field, hex_border_index = border_value
                quad_border = self[quad_border_field]
                hex_border = quad_border.hex_ids.filtered(lambda x: x.index == hex_border_index)
                A_check = (hex.name, border_key, hex_border.name)
                if not hex[border_key]:
                    hex[border_key] = hex_border

    def set_external_ids(self):
        hex_00_01 = self.hex_ids.filtered(lambda x: x.index == 1)
        hex_02_01 = hex_00_01.border_N.border_N
        hex_02_03 = hex_02_01.border_SE.border_SE
        hex_02_05 = hex_02_03.border_S.border_S
        hex_02_07 = hex_02_05.border_SW.border_SW
        hex_02_09 = hex_02_07.border_NW.border_NW
        hex_02_11 = hex_02_09.border_N.border_N

        self.external_ids = [(4, hex_02_01.border_NW.id)]
        self.external_ids = [(4, hex_02_01.border_N.id)]
        self.external_ids = [(4, hex_02_01.border_NE.id)]

        self.external_ids = [(4, hex_02_03.border_N.id)]
        self.external_ids = [(4, hex_02_03.border_NE.id)]
        self.external_ids = [(4, hex_02_03.border_SE.id)]

        self.external_ids = [(4, hex_02_05.border_NE.id)]
        self.external_ids = [(4, hex_02_05.border_SE.id)]
        self.external_ids = [(4, hex_02_05.border_S.id)]

        self.external_ids = [(4, hex_02_07.border_SE.id)]
        self.external_ids = [(4, hex_02_07.border_S.id)]
        self.external_ids = [(4, hex_02_07.border_SW.id)]

        self.external_ids = [(4, hex_02_09.border_S.id)]
        self.external_ids = [(4, hex_02_09.border_SW.id)]
        self.external_ids = [(4, hex_02_09.border_NW.id)]

        self.external_ids = [(4, hex_02_11.border_SW.id)]
        self.external_ids = [(4, hex_02_11.border_NW.id)]
        self.external_ids = [(4, hex_02_11.border_N.id)]

        stop=0
