from odoo import models


class CreatureType(models.Model):
    _name = "creature.type"
    _inherit = ['creature.type', 'mixin.import.csv']
