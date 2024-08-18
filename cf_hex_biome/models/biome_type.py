from odoo import fields, models


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
        selection=[
            ("active", "Attivo"),
            ("future", "Dopo"),
            ("doubtful", "Non attivare"),
            ("upcoming", "A breve"),
        ],
        default="active",
        help="Stato di attivazione",
    )

    good_evil_axis = fields.Selection(
        string="Bene/Male",
        selection=[
            ("good", "Bene"),
            ("evil", "Male"),
            ("neutral", "Neutrale"),
        ],
        default=None,
        help="Asse Bene/Male. Se il bioma non è incline verso un allineamento specifico lasciare vuoto il campo.",
    )

    cosmology = fields.Selection(
        string="Cosmologia",
        selection=[
            ("external", "Esterno"),
            ("mirror", "Specchio"),
            ("elemental", "Elementale"),
        ],
        default=None,
        help="Posizione cosmologica del Bioma. Se il bioma si può trovare ovunque lasciare vuoto il campo",
    )

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""
        vals = {
            "name": row.get('name'),
            "speed_of_travel": row.get('speed_of_travel'),
            "cd_food": row.get('cd_food'),
            "cd_water": row.get('cd_water'),
            "cd_navigation": row.get('cd_navigation'),
            "color": row.get('color'),
            "state": row.get('state'),
            "cosmology": row.get('cosmology'),
            "good_evil_axis": row.get('good_evil_axis'),
        }
        return vals
