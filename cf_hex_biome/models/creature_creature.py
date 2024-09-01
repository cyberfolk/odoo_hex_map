import logging

from odoo import fields, models, api, Command
from ..utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _name = "creature.creature"
    _inherit = 'read.csv.mixin'
    _description = "Creatura"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome generico della creatura per come è registrata sui manuali."
    )

    _sql_constraints = [
        ('unique_creature_creature_name', 'UNIQUE(name)', 'Il nome della creatura deve essere univoco!')
    ]

    cr = fields.Float(
        string="Grado Sfida",
        required=True,
        help="Grado sfida della creatura."
    )

    exp = fields.Float(
        string="Exp",
        compute="_compute_exp",
        help="Esperienza ottenuta eliminando la creatura."
    )

    link_5et = fields.Char(
        string="Link 5et",
        help="Link al form della creatura su 5etools per avere maggiori dettagli."
    )

    is_skip = fields.Boolean(
        string="Sconosciuta",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è sconosciuta dalla maggior parte dei DM. Considera creature più note.",
        store=True
    )

    is_cool = fields.Boolean(
        string="Interessante",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è molto interessante, e funziona bene per creare atmosfera.",
        store=True
    )

    is_endemic = fields.Boolean(
        string="Endemico",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è una specie endemica del bioma, ed è aggressiva.",
        store=True
    )

    is_boss = fields.Boolean(
        string="Boss",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è un boss di fine Quest.",
        store=True
    )

    is_not_violent = fields.Boolean(
        string="Non violento",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è non violenta, potrebbe sapere combattere, ma non attaccherebbe per prima.",
        store=True
    )

    is_innocuous = fields.Boolean(
        string="Innocuo",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è innocua, anche se attacca non sarebbe una minaccia.",
        store=True
    )

    is_social = fields.Boolean(
        string="Sociale",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura fa parte di una struttura sociale organizzata.",
        store=True
    )

    tag_ids = fields.Many2many(
        comodel_name="creature.tag",
        string="Tag",
        help="Tag della creatura"
    )

    type_id = fields.Many2one(
        comodel_name="creature.type",
        string="Tipo",
        help="Tipo di creatura"
    )

    biome_high_prob_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_biome_high_prob_rel",  # Specify a unique relation name
        string="Biomi %Alta",
        help="Biomi con Alta probabilità di trovare la creatura."
    )

    biome_low_prob_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_biome_low_prob_rel",  # Specify a unique relation name
        string="Biomi %Bassa",
        help="Biomi con Bassa probabilità di trovare la creatura."
    )

    faction_ids = fields.Many2many(
        comodel_name="faction.faction",
        relation="faction_faction_creature_creature_rel",
        string="Fazioni",
        help="Fazioni della Creatura",
    )

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        string="Biomi",
        compute="_compute_biome_ids",
        help="Lista che comprende Biomi %Bassa e Biomi %Alta.",
        store=True
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Creatura",
    )

    @api.depends("cr")
    def _compute_exp(self):
        for record in self:
            record.exp = MAP_CR_EXP[str(record.cr)]

    @api.depends("biome_high_prob_ids", "biome_low_prob_ids")
    def _compute_biome_ids(self):
        for record in self:
            record.biome_ids = record.biome_high_prob_ids + record.biome_low_prob_ids

    @api.depends("tag_ids")
    def _compute_boolean_tag(self):
        for record in self:
            record.is_endemic = True if "Endemico" in record.tag_ids.mapped("name") else False
            record.is_boss = True if "Boss" in record.tag_ids.mapped("name") else False
            record.is_not_violent = True if "Non Violento" in record.tag_ids.mapped("name") else False
            record.is_social = True if "Sociale" in record.tag_ids.mapped("name") else False
            record.is_skip = True if "Sconosciuto" in record.tag_ids.mapped("name") else False
            record.is_cool = True if "Interessante" in record.tag_ids.mapped("name") else False
            record.is_innocuous = True if "Innocuo" in record.tag_ids.mapped("name") else False
