from odoo import api, fields, models
from ..utility.constant import BORDERS_MAP
from ..utility.constant import EXTERNAL_BORDERS_MAP
from ..utility.constant import HEX_MISSING_INDEX
from ..utility.constant import SPECULAR_BORDERS_MAP
from ..utility.odoo_to_json import obj_odoo_to_json
import json

class Quadrant(models.Model):
    _name = "hex.quad"
    _inherit = ['hex.mixin']
    _description = "Quadrant, contains Hexagons."

    macro_id = fields.Many2one(
        comodel_name='hex.macro',
        string="Macro Area",
    )

    hex_list = fields.Json(
        string="Hex list",
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='quad_id',
    )

    missing_ids = fields.Many2many(
        comodel_name='hex.hex',
        relation='quad_hex_missing_rel',
        string="Missing IDs"
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

    @api.depends('index')
    def _compute_code(self):
        for rec in self:
            if rec.index:
                rec.code = (chr(ord('A') + rec.index - 1))
            else:
                rec.code = 'void'

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
        quad = super(Quadrant, self).create(vals)
        quad.name = f"Quadrante {quad.code}"
        if quad.code == 'void':
            return quad
        if not quad.hex_list:
            return quad
        for index in quad.hex_list:
            hex_vals = {
                'quad_id': quad.id,
                'index': index,
                'color': quad.color,
            }
            hex_id = self.env['hex.hex'].create(hex_vals)
            hex_id.name = hex_id.code
            quad.hex_ids = [(4, hex_id.id)]
        return quad

    def set_hexs_borders(self):
        """Impostare i bordi degli Esagoni. Setta a void i bordi degli esagoni esterni."""
        hex_void = self.env.ref('cf_hex_base.hex_hex_void')
        index_to_hex = {x.index: x for x in self.hex_ids}  # Crea un dizionario per mappare gli index agli esagoni
        for hex in self.hex_ids:
            borders = BORDERS_MAP[hex.index]
            hex.border_N = index_to_hex.get(borders[0]) or hex_void
            hex.border_NE = index_to_hex.get(borders[1]) or hex_void
            hex.border_SE = index_to_hex.get(borders[2]) or hex_void
            hex.border_S = index_to_hex.get(borders[3]) or hex_void
            hex.border_SW = index_to_hex.get(borders[4]) or hex_void
            hex.border_NW = index_to_hex.get(borders[5]) or hex_void

    def set_hexs_external_borders(self):
        """Impostare i bordi degli Esagoni esterni."""
        filtered_hex_ids = self.hex_ids.filtered(lambda r: r.index != 1)
        for hex in filtered_hex_ids:
            hex_external_borders = EXTERNAL_BORDERS_MAP[hex.index]
            for border_key, border_value in hex_external_borders.items():
                quad_border_field, hex_border_index = border_value
                quad_border = self[quad_border_field]
                hex_border = quad_border.hex_ids.filtered(lambda x: x.index == hex_border_index)
                if hex[border_key].code == 'void' and hex_border:
                    hex[border_key] = hex_border

    @api.model
    def get_json_external_hexs(self, quad_id):
        """Metodo richiamato dal orm di quad.js
            :param quad_id: Id quadrante.
            :return: Json degli esagoni esterni."""
        self_quad = self.env['hex.quad'].browse(quad_id)[0]
        hex_00_01 = self_quad.hex_ids.filtered(lambda x: x.index == 1)
        hex_02_01 = hex_00_01.border_N.border_N
        hex_02_03 = hex_02_01.border_SE.border_SE
        hex_02_05 = hex_02_03.border_S.border_S
        hex_02_07 = hex_02_05.border_SW.border_SW
        hex_02_09 = hex_02_07.border_NW.border_NW
        hex_02_11 = hex_02_09.border_N.border_N
        hex_list = [
            hex_02_01.border_NW, hex_02_01.border_N, hex_02_01.border_NE,
            hex_02_03.border_N, hex_02_03.border_NE, hex_02_03.border_SE,
            hex_02_05.border_NE, hex_02_05.border_SE, hex_02_05.border_S,
            hex_02_07.border_SE, hex_02_07.border_S, hex_02_07.border_SW,
            hex_02_09.border_S, hex_02_09.border_SW, hex_02_09.border_NW,
            hex_02_11.border_SW, hex_02_11.border_NW, hex_02_11.border_N
        ]
        json_hex_list = obj_odoo_to_json(hex_list)
        return json_hex_list

    def set_missing_ids(self):
        """Popola il campo che contiene gli esagoni mancanti."""
        all_index = list(range(1, 20))
        missing_index_list = list(set(all_index) - set(self.hex_ids.mapped('index')))
        for missing_index in missing_index_list:
            border_quad, target_index, borders = HEX_MISSING_INDEX[missing_index]
            missing_hex = self[border_quad].hex_ids.filtered(lambda x: x.index == target_index)
            self.missing_ids = [(4, missing_hex.id)]

            for border_key, border_idex in borders.items():
                target_hex = self.hex_ids.filtered(lambda x: x.index == border_idex)
                missing_hex[border_key] = target_hex
                specular_borders_key = SPECULAR_BORDERS_MAP[border_key]
                target_hex[specular_borders_key] = missing_hex
