# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError

from odoo import api, fields, models


class Hex(models.Model):
    _name = "hex.hex"
    _description = "Hexagonal cell"

    name = fields.Char(
        string='Name',
    )

    code = fields.Char(
        string='Code',
        compute='_compute_code',
    )

    quad_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant",
    )

    circle_order = fields.Integer(
        string='Circle Order',
        compute='_compute_circle_order',
    )

    circle_number = fields.Integer(
        string='Circle Number',
        compute='_compute_circle_number',
    )

    index = fields.Integer(
        string='Index',
        help="Il valore di 'index' deve essere compreso tra 1 e 19.",
    )

    @api.constrains('index')
    def _check_index(self):
        for record in self:
            if record.index < 1 or record.index > 19:
                raise ValidationError("Il valore di 'index' deve essere compreso tra 1 e 19.")

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                record.name = record.code

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            code = f"{record.quad_id.code}"
            code += f".{str(record.circle_order).zfill(2)}"
            code += f".{str(record.circle_number).zfill(2)}"
            record.code = code

    @api.depends('index')
    def _compute_circle_order(self):
        for record in self:
            if record.index == 1:
                record.circle_order = 0
            elif 2 <= record.index <= 7:
                record.circle_order = 1
            elif 8 <= record.index <= 19:
                record.circle_order = 2
            else:
                record.circle_order = None

    @api.depends('index')
    def _compute_circle_number(self):
        for record in self:
            if record.index == 1:
                record.circle_number = 1
            elif 2 <= record.index <= 7:
                record.circle_number = record.index - 1
            elif 8 <= record.index <= 19:
                record.circle_number = record.index - 7
            else:
                record.circle_number = None