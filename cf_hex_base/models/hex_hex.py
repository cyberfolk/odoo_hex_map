from odoo import api, fields, models


class Hex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.mixin']
    _description = "Hexagonal cell"

    quad_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant",
    )

    border_N = fields.Many2one(
        comodel_name='hex.hex',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.hex',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.hex',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.hex',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.hex',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.hex',
        string="NW",
        help="Confine Nord-Ovest"
    )

    @api.depends('index')
    def _compute_code(self):
        for record in self:
            if record.index:
                code = f"{record.quad_id.code}"
                code += f".{str(record.circle_order).zfill(2)}"
                code += f".{str(record.circle_number).zfill(2)}"
            else:
                code = 'void'
            record.code = code

    @api.model
    def change_hex_color(self, hex_id, current_color):
        """Metodo richiamato dal orm di view_macro.js
           Cambia il colore di un hex_id con current_color"""

        _hex = self.env['hex.hex'].browse(hex_id)
        _hex.color = current_color
