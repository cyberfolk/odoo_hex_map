import json
from odoo import api, fields, models, Command


class HexScript(models.Model):
    _name = "hex.script"
    _description = "Script Cell"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Hex-Script"
    )

    biome_id = fields.Many2one(
        comodel_name='biome.biome',
        string="Biome",
        help="Bioma contenuto in questo Hex-Script"
    )

    hex_id = fields.Many2one(
        comodel_name='hex.hex',
        string="Esagono",
        help="Esagono relativo a questo Hex-Script"
    )

    sml = fields.Integer(
        string="SML",
        help="Difficoltà Hex-Script. Calcolata come 'Scontro Mortale per 4 PG di Livello SML'"
    )

