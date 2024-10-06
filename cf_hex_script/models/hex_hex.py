import json

from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    hex_script_id = fields.Many2one(
        comodel_name='hex.script',
        string="Hex Script",
        help="Hex-Script contenuto in questo Hex"
    )
