from odoo import models


class CreatureTag(models.Model):
    _name = "creature.tag"
    _inherit = ['creature.tag', 'mixin.import.csv']
