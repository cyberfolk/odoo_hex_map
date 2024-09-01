from odoo import models


class StructureStructure(models.Model):
    _name = "structure.structure"
    _inherit = ['structure.structure', 'mixin.import.csv']
