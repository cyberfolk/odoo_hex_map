import logging

from odoo import fields, models, api
from ..utility.selection import STATE_LIST, GOOD_EVIL_LIST, COSMOLOGY_LIST

_logger = logging.getLogger(__name__)


class FactionFaction(models.Model):
    _name = "faction.faction"
    _description = "Fazione"

    _sql_constraints = [
        ('unique_faction_faction_name', 'UNIQUE(name)', 'Il nome della fazione deve essere univoco!'),
        ('unique_faction_faction_code', 'UNIQUE(code)', 'Il code della fazione deve essere univoco!')
    ]

    # region FIELD -----------------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome della fazione",
    )

    code = fields.Char(
        string="Codice",
        help="Codice della fazione",
    )

    child_ids = fields.One2many(
        comodel_name="faction.faction",
        inverse_name="parent_id",
        string="Fazioni figlie",
        help="Fazioni figlie della fazione",
    )

    parent_id = fields.Many2one(
        comodel_name="faction.faction",
        string="Fazione Padre",
        help="Fazione Padre della fazione",
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
        help="Asse Bene/Male. Se la fazione non è incline verso un allineamento specifico lasciare vuoto il campo.",
    )

    cosmology = fields.Selection(
        string="Cosmologia",
        selection=COSMOLOGY_LIST,
        default=None,
        help="Posizione cosmologica del Bioma. Se la fazione si può trovare ovunque lasciare vuoto il campo",
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        relation="faction_faction_creature_creature_rel",
        string="Creature",
        help="Creature della fazione",
    )

    encounter_ids = fields.One2many(
        comodel_name="creature.encounter",
        inverse_name="faction_id",
        string="Scontri",
        help="Scontri della fazione",
    )

    is_child = fields.Boolean(
        string="È Figlio",
        help="È una Fazione figlio di un'altra Fazione Padre",
        compute="_compute_is_child",
        store=True,
    )

    is_parent = fields.Boolean(
        string="È Padre",
        help="È una Fazione Padre di altre Fazione Figlio",
        compute="_compute_is_parent",
        store=True,
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della fazione",
    )

    desc_creature = fields.Html(
        string="Descrizione creature",
        compute="_compute_desc_creature",
    )

    # Info base:
    n01_years_in_region = fields.Text(string="Da quanti anni sono nella regione?")
    n02_daily_operations = fields.Text(string="Quali sono le loro operazioni quotidiane?")
    n03_feeding_habits = fields.Text(string="Come si nutrono?")

    # Gerarchia e struttura sociale
    n04_handling_threats = fields.Text(string="Come si occupano delle normali minacce?")
    n05_answering_powers = fields.Text(string="A quali poteri rispondono?")
    n06_scouts = fields.Text(string="Hanno degli esploratori?")

    # Territorio e influenza
    n07_key_positions_controlled = fields.Text(string="Che posizioni chiave controllano?")
    n08_boundary_marking = fields.Text(string="Come segnano i loro confini?")
    n09_territory_claiming = fields.Text(string="Come rivendicano il loro territorio?")

    # Basi
    n10_base_structure = fields.Text(string="Che Struttura è la loro Base?")
    n11_base_origin = fields.Text(string="L'hanno costruita loro o esisteva già?")
    n12_base_purpose = fields.Text(string="Perché viene utilizzata?")

    # Motivazioni
    n13_long_term_goals = fields.Text(string="Obbiettivi a Lungo Termine?")
    n14_short_term_goals = fields.Text(string="Obbiettivi a Breve Termine?")
    n15_motivations = fields.Text(string="Da che motivazioni sono spinti?")
    n16_goal_strategy = fields.Text(string="In che modo intendono Raggiungerli?")

    # Extra
    n17_leader_view_of_pcs = fields.Text(string="I leader come vede i PG?")
    n18_contact_with_pcs = fields.Text(string="Come entrano in contatto coi PG?")
    n19_possible_developments = fields.Text(string="Possibili sviluppi della Fazione?")
    n20_faction_theme = fields.Text(string="Tema della Fazione?")

    # endregion FIELD --------------------------------------------------------------------------------------------------

    # region COMPUTED METHOD -------------------------------------------------------------------------------------------
    @api.depends("child_ids", "parent_id")
    def _compute_is_child(self):
        for rec in self:
            rec.is_child = True if rec.parent_id else False

    @api.depends("child_ids", "parent_id")
    def _compute_is_parent(self):
        for rec in self:
            rec.is_parent = True if rec.child_ids else False

    @api.depends("creature_ids")
    def _compute_desc_creature(self):
        for rec in self:
            creatures = rec.creature_ids.filtered(lambda x: x.description and x.description != '<p><br></p>')
            creatures = sorted(creatures, key=lambda x: len(x.description))
            content = "".join([
                f"""
                <div class="col-3">
                    <h2>{creature.name}</h2>
                    <p>{creature.description}</p>
                </div>
                """
                for creature in creatures if creature and creature.description
            ])
            rec.desc_creature = f"""<div class="row">{content}</div>""" if content else "Nessuna creatura"

    # endregion COMPUTED METHOD ----------------------------------------------------------------------------------------
