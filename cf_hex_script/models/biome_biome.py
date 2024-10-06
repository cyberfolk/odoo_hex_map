from odoo import fields, models, api


class BiomeBiome(models.Model):
    _inherit = "biome.biome"

    hex_script_ids = fields.One2many(
        comodel_name="hex.script",
        inverse_name="biome_id",
        string="Elenco degli Hex-Scripts che hanno questo Bioma",
    )
