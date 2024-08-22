import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _name = "todo"
    _description = "TODO"

    name = fields.Char(
        string="Nome",
    )
    description = fields.Text(
        string="Descrizione",
    )
