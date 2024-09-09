import json

from odoo import fields, models, api
from ..utility.constant import BORDERS_MAP


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
        """Metodo richiamato dal orm di view_macro.js
            :return: Json della Macro-Area."""
        # Ho ottimizzato il codice recuperando i dati con solo 3 query al DB
        self_macro = self.env['hex.macro'].browse(1)

        quad_fields = ['id', 'code', 'index', 'polygon', 'hex_ids']
        hex_fields = ['id', 'code', 'index', 'color', 'asset_ids']

        # Otteniamo tutti i quad e i relativi hex in una singola query
        quads = self_macro.quad_ids.read(quad_fields)
        hex_map = {quad['id']: self.env['hex.hex'].browse(quad['hex_ids']).read(hex_fields) for quad in quads}

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

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            record.code = (chr(ord('A') + record.index - 1))

    def set_quads_borders(self):
        """Impostare i bordi dei quadranti. Dal secondo cerchio in poi ci potrebbero essere bordi che non
        confinano con nulla, in quel caso quei bordi verranno settati a void."""
        quad_void = self.env.ref('cf_hex_base.hex_quad_void')
        index_to_quad = {x.index: x for x in self.quad_ids}  # Crea un dizionario per mappare gli index agli esagoni
        A_debug = ""
        for quad in self.quad_ids:
            borders = BORDERS_MAP[quad.index]
            quad.border_N = index_to_quad.get(borders[0]) or quad_void
            quad.border_NE = index_to_quad.get(borders[1]) or quad_void
            quad.border_SE = index_to_quad.get(borders[2]) or quad_void
            quad.border_S = index_to_quad.get(borders[3]) or quad_void
            quad.border_SW = index_to_quad.get(borders[4]) or quad_void
            quad.border_NW = index_to_quad.get(borders[5]) or quad_void

            # SCOMMENTARE PER DEBUG
            # A_debug += (f"Borders {quad.code}: {quad.border_N.code} {quad.border_NE.code} {quad.border_SE.code}"
            #             f"{quad.border_S.code} {quad.border_SW.code} {quad.border_NW.code}\n")
        return A_debug
