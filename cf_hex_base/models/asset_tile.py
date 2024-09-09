import json
import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AssetTile(models.Model):
    _name = "asset.tile"
    _description = "Asset Tile"

    name = fields.Char(string="Nome", required=True)
    image = fields.Image(string="Image", attachment=True)  # Usa attachment=True per il filestore
    sub_dir = fields.Char(string="Subdir", default="")
    hex_ids = fields.Many2many(comodel_name="hex.hex", string="Hexagons")

    @api.model
    def get_json_tiles_kit(self):
        """Metodo richiamato dal orm di view_macro.js
            :return: Json del TilesKit."""
        asset_tiles = list(self.env['asset.tile'].search([]))
        asset_tiles_dikt = [{'name': x.name, 'sub_dir': x.sub_dir, 'id': x.id} for x in asset_tiles]
        tiles_kit = {}
        for tile in asset_tiles_dikt:
            sub_dirs = tile.pop('sub_dir').split('/')
            current_level = tiles_kit

            # Itera su tutte le sottodirectory per creare la struttura annidata
            for sub_dir in sub_dirs:
                if sub_dir not in current_level:
                    current_level[sub_dir] = {}
                current_level = current_level[sub_dir]

            # Aggiungi il tile all'ultimo livello
            if 'tiles' not in current_level:
                current_level['tiles'] = []
            current_level['tiles'].append(tile)

        json_tiles_kit = json.dumps(tiles_kit)
        return json_tiles_kit
