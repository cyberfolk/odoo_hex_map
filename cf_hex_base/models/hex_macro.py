import json

from odoo import fields, models, api
from ..utility.constant import BORDERS_MAP
from ..utility.constant import QUAD_LIST


class MacroArea(models.Model):
    _name = "hex.macro"
    _description = "Macro-Area, contains Quadrants."

    name = fields.Char(
        string='Name',
    )

    quad_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='macro_id',
    )

    @api.model
    def get_json_macro(self):
        """Metodo richiamato dal orm di view_macro.js
            :return: Json della Macro-Area."""
        self_macro = self.env['hex.macro'].browse(1)
        quad_fields = ['id', 'code', 'index', 'polygon', 'hex_ids']
        hex_fields = ['id', 'code', 'index', 'color', 'hex_asset_id']

        # Otteniamo tutti i quad e i relativi hex in una singola query
        quads = self_macro.quad_ids.read(quad_fields)
        hex_map = {quad['id']: self.env['hex.hex'].browse(quad['hex_ids']).read(hex_fields) for quad in quads}

        # Aggiungo le info relative a gli hex_asset negli hex
        hex_asset_fields = ['asset_id', 'rotation']
        hex_assets = self.env['hex.asset.tile'].search([]).read(hex_asset_fields)
        hex_assets_map = {x['id']: {'tile_id': x['asset_id'][0], 'rotation': x['rotation']} for x in hex_assets}
        for k, v in hex_map.items():
            for _hex in v:
                if _hex['hex_asset_id']:
                    _id = _hex['hex_asset_id'][0]
                    _hex['hex_asset_id'] = hex_assets_map[_id]

        dict_macro = {
            'quad_ids': [{
                'id': quad['id'],
                'code': quad['code'],
                'index': quad['index'],
                'polygon': quad['polygon'],
                'hex_ids': hex_map[quad['id']],
            } for quad in quads]
        }
        json_macro = json.dumps(dict_macro)
        return json_macro

    def set_quads_borders(self):
        """Impostare i bordi dei quadranti. Dal secondo cerchio in poi ci potrebbero essere bordi che non
        confinano con nulla, in quel caso quei bordi verranno settati a void."""
        quad_void = self.env.ref('cf_hex_base.hex_quad_void')
        index_to_quad = {x.index: x for x in self.quad_ids}  # Crea un dizionario per mappare gli index agli esagoni
        for quad in self.quad_ids:
            borders = BORDERS_MAP[quad.index]
            quad.border_N = index_to_quad.get(borders[0]) or quad_void
            quad.border_NE = index_to_quad.get(borders[1]) or quad_void
            quad.border_SE = index_to_quad.get(borders[2]) or quad_void
            quad.border_S = index_to_quad.get(borders[3]) or quad_void
            quad.border_SW = index_to_quad.get(borders[4]) or quad_void
            quad.border_NW = index_to_quad.get(borders[5]) or quad_void

    @api.model_create_multi
    def create(self, vals_list):
        """Serve per settare:
            - La lista dei Quadranti e relative liste degli Esagoni,
            - I confini dei Quadranti,
            - I confini interni degli Esagoni
            - I confini esterni degli Esagoni
            - La lista degli Esagoni mancanti
        """
        macro = super().create(vals_list)
        for quad_dict in QUAD_LIST:
            quad = self.env['hex.quad'].create(quad_dict)
            macro.quad_ids = [(4, quad.id)]
            stop = 0
        stop = 0
        macro.set_quads_borders()
        for quad in macro.quad_ids:
            quad.set_hexs_borders()
        for quad in macro.quad_ids:
            quad.set_hexs_external_borders()
        for quad in macro.quad_ids:
            quad.set_missing_ids()
        return macro
