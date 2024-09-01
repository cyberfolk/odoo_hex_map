from odoo import models


class CreatureCreature(models.Model):
    _name = "creature.creature"
    _inherit = ['creature.creature', 'mixin.import.csv']
