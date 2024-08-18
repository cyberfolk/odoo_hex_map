from odoo import fields, models


class CreatureTag(models.Model):
    _name = "creature.tag"
    _inherit = 'read.csv.mixin'
    _description = "Tag per creature"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Tag per creature"
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        string="Creature",
        help="Creature con questo tag"
    )
