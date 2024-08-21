import logging

from odoo import fields, models, api, Command
from ..constants.exp import MAP_QTY_MOD, MAP_LEVEL_EXP, MAP_SML_QTY, LIST_CR

_logger = logging.getLogger(__name__)


class CreatureEncounter(models.Model):
    _name = "creature.encounter"
    _inherit = 'read.csv.mixin'
    _description = "Scontro"

    name = fields.Char(
        string="Nome",
        help="Nome dello scontro.",
        compute="_compute_name"
    )

    line_ids = fields.One2many(
        comodel_name="creature.encounter.line",
        inverse_name="encounter_id",
        string="Linee",
        help="Linee dello scontro.",
    )

    exp_sum = fields.Integer(
        string="Exp Somma",
        compute="_compute_exp_sum",
        help="Somma delle esperienza delle singole creature.",
    )

    tot_creatures = fields.Integer(
        string="Totale Creature",
        compute="_compute_tot_creatures",
        help="Totale creature presenti nelle righe.",
    )

    exp_adj = fields.Integer(
        string="Exp Adjusted",
        compute="_compute_exp_adj",
        help="Esperienza dello scontro tenendo conto del modificatore per il numero di creature.",
    )

    sml = fields.Char(
        string="SML",
        compute="_compute_sml",
        help="Scontro Mortale per 4 PG di Livello 'SML'",
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        compute="_compute_creature_ids",
        string="Creature",
        help="Creature che compongono lo scontro.",
    )

    biome_type_ids = fields.Many2many(
        comodel_name="biome.type",
        compute="_compute_biome_type_ids",
        string="Tipi di Bioma",
        help="Tipi di Bioma dove può verificarsi lo scontro.",

    )

    @api.depends("line_ids")
    def _compute_name(self):
        for record in self:
            record.name = " + ".join(filter(None, record.line_ids.mapped("name")))
            if not record.name:
                record.name = f"Nome temporaneo"

    @api.depends("line_ids")
    def _compute_exp_sum(self):
        for record in self:
            record.exp_sum = sum(line.exp_sum for line in record.line_ids)
            if not record.exp_sum:
                record.exp_sum = 0

    @api.depends("line_ids")
    def _compute_tot_creatures(self):
        for record in self:
            record.tot_creatures = sum(line.creature_qty for line in record.line_ids)
            if not record.tot_creatures:
                record.tot_creatures = 0

    @api.depends("line_ids")
    def _compute_exp_adj(self):
        for record in self:
            record.exp_adj = record.exp_sum * MAP_QTY_MOD[str(record.tot_creatures)]
            if not record.exp_adj:
                record.exp_adj = 0

    @api.depends("line_ids")
    def _compute_sml(self):
        for record in self:
            MAP_SML_EXP = {k: v[3] * 4 for k, v in MAP_LEVEL_EXP.items()}
            steps = sorted(MAP_SML_EXP.values()) + [float('inf')]
            for i in range(len(steps) - 1):
                if steps[i] <= record.exp_adj < steps[i + 1]:
                    record.sml = i
                    break
            if not record.sml:
                self.sml = 0

    @api.depends("line_ids")
    def _compute_creature_ids(self):
        for record in self:
            for line in record.line_ids:
                record.creature_ids |= line.creature_id
            if not record.creature_ids:
                self.creature_ids = []

    @api.depends("line_ids")
    def _compute_biome_type_ids(self):
        for record in self:
            if record.creature_ids and record.creature_ids.biome_ids:
                record.biome_type_ids = record.creature_ids.biome_ids
            else:
                record.biome_type_ids = []  # or any other default value or action

    def create_sml_encounter(self):
        _logger.info("START create_sml_encounter")
        not_violent = self.env['creature.tag'].search([("name", "=", "Non Violento")]).id
        inoffensive = self.env['creature.tag'].search([("name", "=", "Innocuo")]).id
        skip_tags = [not_violent, inoffensive]
        for sml, qtys in MAP_SML_QTY.items():
            _logger.info(f"** START SML {sml}")
            for i, qty in enumerate(qtys):
                if not qty or qty > 11:
                    continue
                cr = LIST_CR[i]
                creatures = self.env["creature.creature"].search([("cr", "=", cr), ("tag_ids", "not in", skip_tags)])
                _logger.info(f"**** START SML {sml} - CR {cr} - FIND {len(creatures)} CREATURES")
                for n, creature in enumerate(creatures):
                    encounter = self.create({
                        "line_ids": [Command.create({
                            'creature_qty': qty,
                            'creature_id': creature.id
                        })]
                    })
                    _logger.info(f"****** ({n + 1}/{len(creatures)}) CREATE {encounter.name}")
                _logger.info(f"**** END SML {sml} - CR {cr}")
            _logger.info(f"** END SML {sml}")
        _logger.info("END create_sml_encounter")
