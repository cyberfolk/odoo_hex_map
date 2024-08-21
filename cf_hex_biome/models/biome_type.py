from odoo import fields, models, api

STATE_LIST = [
    ("active", "Attivo"),
    ("future", "Dopo"),
    ("doubtful", "Non attivare"),
    ("upcoming", "A breve"),
]

GOOD_EVIL_LIST = [
    ("good", "Bene"),
    ("evil", "Male"),
    ("neutral", "Neutrale"),
]

COSMOLOGY_LIST = [
    ("external", "Esterno"),
    ("mirror", "Specchio"),
    ("elemental", "Elementale"),
]
REVERSE_STATE_LIST = {v: k for k, v in STATE_LIST}
REVERSE_GOOD_EVIL_LIST = {v: k for k, v in GOOD_EVIL_LIST}
REVERSE_COSMOLOGY_LIST = {v: k for k, v in COSMOLOGY_LIST}


class BiomeType(models.Model):
    _name = "biome.type"
    _inherit = 'read.csv.mixin'
    _description = "Tipo di Bioma"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Bioma"
    )

    _sql_constraints = [
        ('unique_biome_type_name', 'UNIQUE(name)', 'Il nome del tipo di Bioma deve essere univoco!')
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

    creature_inoffensive = fields.Many2many(
        string="Creature Innocue",
        comodel_name="creature.creature",
        compute="_compute_creature_inoffensive",
        help="Creature Innocue presenti nel bioma."
    )

    creature_not_violent = fields.Many2many(
        string="Creature Non Violente",
        comodel_name="creature.creature",
        compute="_compute_creature_not_violent",
        help="Creature Non Violente presenti nel bioma."
    )

    creature_cool = fields.Many2many(
        string="Creature Interessanti",
        comodel_name="creature.creature",
        compute="_compute_creature_cool",
        help="Creature Interessanti presenti nel bioma."
    )

    creature_endemic = fields.Many2many(
        string="Creature Endemiche",
        comodel_name="creature.creature",
        compute="_compute_creature_endemic",
        help="Creature Endemiche presenti nel bioma."
    )

    def _compute_creature_inoffensive(self):
        for record in self:
            creature = record.creature_high_prob_ids | record.creature_low_prob_ids
            tag_inoffensive_id = self.env['creature.tag'].search([("name", "=", "Innocuo")])
            self.creature_inoffensive = creature.filtered(lambda x: tag_inoffensive_id in x.tag_ids)

    def _compute_creature_not_violent(self):
        for record in self:
            creature = record.creature_high_prob_ids | record.creature_low_prob_ids
            tag_not_violent_id = self.env['creature.tag'].search([("name", "=", "Non Violento")])
            self.creature_not_violent = creature.filtered(lambda x: tag_not_violent_id in x.tag_ids)

    def _compute_creature_cool(self):
        for record in self:
            creature = record.creature_high_prob_ids | record.creature_low_prob_ids
            self.creature_cool = creature.filtered(lambda x: x.cool)

    def _compute_creature_endemic(self):
        for record in self:
            creature = record.creature_high_prob_ids | record.creature_low_prob_ids
            tag_endemic_id = self.env['creature.tag'].search([("name", "=", "Endemico")])
            self.creature_endemic = creature.filtered(lambda x: tag_endemic_id in x.tag_ids)

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""
        vals = {
            "name": row.get('Nome'),
            "speed_of_travel": row.get('Velocità'),
            "cd_food": row.get('CD Cibo'),
            "cd_water": row.get('CD Acqua'),
            "cd_navigation": row.get('CD Navigazione'),
            "color": row.get('Colore'),
            "state": REVERSE_STATE_LIST.get(row.get('Stato')),
            "cosmology": REVERSE_COSMOLOGY_LIST.get(row.get('Cosmologia')),
            "good_evil_axis": REVERSE_GOOD_EVIL_LIST.get(row.get('Bene/Male')),
        }
        return vals


