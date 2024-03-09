from odoo import api, fields, models


class HexMixin(models.AbstractModel):
    _name = 'hex.mixin'
    _description = "Abstract class that contains common fields and common behaviors of the main hex-class"

    name = fields.Char(
        string='Name',
    )

    code = fields.Char(
        string='Code',
        compute='_compute_code',
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

    color = fields.Char(
        string='Color',
    )

    @api.depends('code')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.code

    @api.constrains('index')
    def _check_index(self):
        for record in self:
            if record.index < 1 or record.index > 19:
                raise ValidationError("Il valore di 'index' deve essere compreso tra 1 e 19.")

    @api.constrains('name')
    def check_name(self):
        for record in self:
            if not record.name:
                record.name = record.code

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            record.code = (chr(ord('A') + record.index - 1))

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
