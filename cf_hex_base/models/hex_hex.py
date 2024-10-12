import json
from odoo import api, fields, models, Command


class HexAssetTile(models.Model):
    _name = "hex.asset.tile"
    _description = "Hexagonal Asset Tiles"

    rotation = fields.Integer(string="Rotazione")
    asset_id = fields.Many2one(
        comodel_name='asset.tile',
        string="Asset",
        help="Assets contained in this hex"
    )


class Hex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.mixin']
    _description = "Hexagonal cell"

    name = fields.Char(
        string="Name",
        default=lambda self: self.code
    )

    hex_asset_id = fields.Many2one(
        comodel_name='hex.asset.tile',
        string="Hex Asset",
        help="Hex Assets contained in this hex"
    )

    quad_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant",
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
            if record.index:
                code = f"{record.quad_id.code}"
                code += f".{str(record.circle_order).zfill(2)}"
                code += f".{str(record.circle_number).zfill(2)}"
            else:
                code = 'void'
            record.code = code

    @api.model
    def change_hex_color(self, hex_id, current_color):
        """Metodo richiamato dal orm di view_macro.js
           Cambia il colore di un hex_id con current_color"""

        _hex = self.env['hex.hex'].browse(hex_id)
        _hex.color = current_color

    @api.model
    def set_asset_tiles(self, hex_id, current_tile):
        """Metodo richiamato dal orm di view_macro.js
           Setta i parametri di hex_asset su hex_id"""

        _hex = self.env['hex.hex'].browse(hex_id)
        hex_asset_vals = {
            'asset_id': current_tile['tile_id'],
            'rotation': current_tile['rotation']
        }
        if not _hex.hex_asset_id:
            hex_asset = self.env['hex.asset.tile'].create(hex_asset_vals)
            _hex.hex_asset_id = hex_asset.id
        else:
            _hex.hex_asset_id.write(hex_asset_vals)

    @api.model
    def get_json_hex(self):
        """Metodo richiamato dal orm di HexHex.js
            :return: Json del hex."""
        dict_hex = {
            'id': self.id,
            'index': self.index,
            'color': self.color,
            'hex_asset_id': {
                'rotation': self.hex_asset_id.rotation,
                'tile_id': self.hex_asset_id.asset_id.id,
            },
        }

        json_hex = json.dumps(dict_hex)
        return json_hex

