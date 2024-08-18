from odoo import fields, models
from ..data.list_creature_tag import LIST_CREATURE_TAG


class CreatureTag(models.Model):
    _name = "creature.tag"
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

    def popolate_creature_tag(self):
        """Crea i tag per le creature partendo da LIST_CREATURE_TAG
        """
        for tag in LIST_CREATURE_TAG:
            self.env["creature.tag"].create({
                "name": tag
            })
