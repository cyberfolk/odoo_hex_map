from odoo import fields, models, api
from ..utility.color import is_dark
from ..utility.selection import STATE_LIST, GOOD_EVIL_LIST, COSMOLOGY_LIST


class BiomeBiome(models.Model):
    _name = "biome.biome"
    _inherit = 'read.csv.mixin'
    _description = "Bioma"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Bioma"
    )

    _sql_constraints = [
        ('unique_biome_biome_name', 'UNIQUE(name)', 'Il nome del Bioma deve essere univoco!')
    ]

    speed_of_travel = fields.Float(
        string="Velocità",
        help="Velocità di viaggio",
        default=1
    )

    cd_food = fields.Integer(
        string="CD Cibo",
        default=13,
        help="CD per trovare cibo",
    )

    cd_water = fields.Integer(
        string="CD Acqua",
        default=13,
        help="CD per trovare Acqua",
    )

    cd_navigation = fields.Integer(
        string="CD Navigazione",
        default=13,
        help="CD per Navigare",
    )

    color = fields.Char(
        string="Colore",
        help="Colore",
        default="#000000"
    )

    structure_ids = fields.Many2many(
        comodel_name="structure.structure",
        string="Strutture",
    )

    state = fields.Selection(
        string="Stato",
        selection=STATE_LIST,
        default="active",
        help="Stato di attivazione",
    )

    good_evil_axis = fields.Selection(
        string="Bene/Male",
        selection=GOOD_EVIL_LIST,
        default=None,
        help="Asse Bene/Male. Se il bioma non è incline verso un allineamento specifico lasciare vuoto il campo.",
    )

    cosmology = fields.Selection(
        string="Cosmologia",
        selection=COSMOLOGY_LIST,
        default=None,
        help="Posizione cosmologica del Bioma. Se il bioma si può trovare ovunque lasciare vuoto il campo",
    )

    creature_high_prob_ids = fields.Many2many(
        comodel_name="creature.creature",
        relation="creature_biome_high_prob_rel",  # Specify a unique relation name
        string="Creature %Alta",
        help="Creature con Alta probabilità di trovarle nel Bioma."
    )

    creature_low_prob_ids = fields.Many2many(
        comodel_name="creature.creature",
        relation="creature_biome_low_prob_rel",  # Specify a unique relation name
        string="Creature %Bassa",
        help="Creature con Bassa probabilità di trovarle nel Bioma."
    )

    creature_innocuous = fields.Many2many(
        string="Creature Innocue",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Innocue presenti nel bioma."
    )

    creature_not_violent = fields.Many2many(
        string="Creature Non Violente",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Non Violente presenti nel bioma."
    )

    creature_cool = fields.Many2many(
        string="Creature Interessanti",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Interessanti presenti nel bioma."
    )

    creature_endemic = fields.Many2many(
        string="Creature Endemiche",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Endemiche presenti nel bioma."
    )

    creature_social = fields.Many2many(
        string="Creature Sociali",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Sociali presenti nel bioma."
    )

    creature_boss = fields.Many2many(
        string="Creature Boss",
        comodel_name="creature.creature",
        compute="_compute_creature_boolean_tag",
        help="Creature Boss presenti nel bioma."
    )

    encounter_ids = fields.Many2many(
        comodel_name="creature.encounter",
        relation="creature_encounter_biome_biome_rel",
        string="Scontri del Bioma",
        help="Scontri che si possono verificare nel bioma.",
    )

    kanban_color_name = fields.Char(
        string="Kanban Colore Nome",
        compute="_compute_kanban_color_name",
        help="Campo utility per impostare il colore del nome del bioma nella vista kanban.",
    )

    @api.depends('color')
    def _compute_kanban_color_name(self):
        for record in self:
            _is_dark = is_dark(record.color)
            record.kanban_color_name = "#ffffff" if _is_dark else "#000000"

    def _compute_creature_boolean_tag(self):
        for record in self:
            creature = record.creature_high_prob_ids | record.creature_low_prob_ids
            self.creature_innocuous = creature.filtered(lambda x: x.is_innocuous)
            self.creature_not_violent = creature.filtered(lambda x: x.is_not_violent)
            self.creature_cool = creature.filtered(lambda x: x.is_cool)
            self.creature_endemic = creature.filtered(lambda x: x.is_endemic)
            self.creature_social = creature.filtered(lambda x: x.is_social)
            self.creature_boss = creature.filtered(lambda x: x.is_boss)
