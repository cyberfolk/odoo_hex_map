from odoo import fields, models


class CreatureType(models.Model):
    _name = "creature.type"
    _inherit = 'read.csv.mixin'
    _description = "Tipi di creature"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Tipo di creature"
    )

    creature_ids = fields.One2many(
        comodel_name="creature.creature",
        inverse_name="type_id",
        string="Creature",
    )
