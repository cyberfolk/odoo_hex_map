from odoo import fields, models
from ..data.list_creature_type import LIST_CREATURE_TYPE


class CreatureType(models.Model):
    _name = "creature.type"
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

    def popolate_creature_type(self):
        """Crea i tag per le creature partendo da LIST_CREATURE_TYPE
        """
        for type_ in LIST_CREATURE_TYPE:
            self.env["creature.type"].create({
                "name": type_
            })
