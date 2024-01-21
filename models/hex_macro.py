# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MacroArea(models.Model):
    _name = "hex.macro"
    _description = "Macro-Area, contains Quadrants."

    name = fields.Char(
        string='Name',
    )

    quadrant_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='macro_id',
    )
