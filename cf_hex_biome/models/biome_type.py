from odoo import fields, models


class BiomeType(models.Model):
    _name = "biome.type"
    _description = "Tipo di Bioma"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Bioma"
    )

    speed_of_travel = fields.Float(
        string="Velocità",
        required=True,
        help="Velocità di viaggio",
        default=1
    )

    cd_food = fields.Integer(
        string="CD Cibo",
        required=True,
        help="CD per trovare cibo",
    )

    cd_water = fields.Integer(
        string="CD Acqua",
        required=True,
        help="CD per trovare Acqua",
    )

    cd_navigation = fields.Integer(
        string="CD Navigazione",
        required=True,
        help="CD per Navigare",
    )

    color = fields.Char(
        string="Colore",
        required=True,
        help="Colore",
        default="#000000"
    )

