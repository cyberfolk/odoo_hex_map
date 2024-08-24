from odoo import fields, models, api


class FactionFaction(models.Model):
    _name = "faction.faction"
    _inherit = 'read.csv.mixin'
    _description = "Fazione"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome della fazione",
    )