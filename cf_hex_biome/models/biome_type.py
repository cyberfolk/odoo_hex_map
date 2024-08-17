from odoo import fields, models
"""
BIOMA	State		Evil/Neutral/Good
Foresta	active	-	-
Coste	active	-	-
Aquatico	active	-	-
Deserto	active	-	-
Prateria	active	-	-
Colline	active	-	-
Montagne	active	-	-
Palude	active	-	-
Artico	active	-	-
Male	future	external	evil
Inferno	future	external	evil
Abisso	future	external	evil
Carceri	future	external	evil
Distese Grige 	future	external	evil
Gehenna	future	external	evil
Acqua	future	elemental	neutral
Aria	future	elemental	neutral
Fuoco	future	elemental	neutral
Terra	future	elemental	neutral
Feywild	upcoming	mirror	neutral
Shadowfell	upcoming	mirror	tending-evil
Vulcano	upcoming	-	-
A Dolce	upcoming	-	-
Giungla	upcoming	-	-
Savana	upcoming	-	-
Cimitero	upcoming	-	tending-evil
Far Realms 	upcoming	external	evil
Space	upcoming	-	-
Astrale	doubtful	external	-
Etereo	doubtful	mirror	-
Limbo	doubtful	external	neutral
Bene	doubtful	external	good
Underdark	doubtful	-	tending-evil
Urban	doubtful	-	-
Dungeon	doubtful	-	-
"""

class BiomeType(models.Model):
    _name = "biome.type"
    _description = "Tipo di Bioma"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Bioma"
    )

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

