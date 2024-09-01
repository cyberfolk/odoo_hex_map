from odoo import models


class BiomeBiome(models.Model):
    _name = "biome.biome"
    _inherit = ['biome.biome', 'mixin.import.csv']
