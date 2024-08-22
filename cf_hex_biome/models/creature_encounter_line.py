import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class CreatureEncounterLine(models.Model):
    _name = "creature.encounter.line"
    _inherit = 'read.csv.mixin'
    _description = "Linee dello scontro"
    _order = 'cr desc'

    name = fields.Char(
        string="Nome",
        help="Nome della linea dello scontro.",
        compute="_compute_name",
    )

    encounter_id = fields.Many2one(
        comodel_name="creature.encounter",
        string="Scontro",
        help="Scontro a cui appartiene la linea.",
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura",
    )

    is_endemic = fields.Boolean(
        string="Endemico",
        related='creature_id.is_endemic',
    )

    creature_qty = fields.Integer(
        string="Quantità",
        required=True,
        help="Quantità della creatura.",
    )

    cr = fields.Float(
        related='creature_id.cr',
        store=True,
        string="Creatura GS",
    )

    exp_single = fields.Float(
        related='creature_id.exp',
        string="Exp Creatura",
    )

    exp_sum = fields.Float(
        string="Exp Somma",
        compute="_compute_exp_sum",
    )

    @api.depends("creature_qty", "creature_id")
    def _compute_exp_sum(self):
        for record in self:
            record.exp_sum = record.creature_qty * record.creature_id.exp
            if not record.exp_sum:
                record.exp_sum = 0

    @api.depends("creature_qty", "creature_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.creature_qty} x {record.creature_id.name}"
            if not record.creature_id:
                record.name = f"Nome temporaneo"
