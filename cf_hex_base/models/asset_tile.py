import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AssetTile(models.Model):
    _name = "asset.tile"
    _description = "Asset Tile"

    name = fields.Char(string="Nome", required=True)
    image = fields.Image(string="Image", attachment=True)  # Usa attachment=True per il filestore
    sub_dir = fields.Char(string="Subdir", default="")
