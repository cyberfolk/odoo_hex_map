import logging

from odoo import fields, models, api
from ..utility.selection import STATE_LIST, GOOD_EVIL_LIST, COSMOLOGY_LIST

_logger = logging.getLogger(__name__)


class FactionFaction(models.Model):
    _name = "faction.faction"
    _inherit = 'import.by.py.mixin'
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

    def get_data_str(self):
        """Scarica i dati delle fazioni nel file 'faction.py' mettendolo nella cartella 'data'."""
        _logger.info("START download_factions_py")

        # Fetch faction and structure the data
        factions = self.search([])
        faction_list = [{
            'name': faction.name,
            'code': faction.code,
            'state': faction.state,
            'cosmology': faction.cosmology,
            'description': str(faction.description),
            'good_evil_axis': faction.good_evil_axis,
            "n01_years_in_region": faction.n01_years_in_region,
            "n02_daily_operations": faction.n02_daily_operations,
            "n03_feeding_habits": faction.n03_feeding_habits,
            "n04_handling_threats": faction.n04_handling_threats,
            "n05_answering_powers": faction.n05_answering_powers,
            "n06_scouts": faction.n06_scouts,
            "n07_key_positions_controlled": faction.n07_key_positions_controlled,
            "n08_boundary_marking": faction.n08_boundary_marking,
            "n09_territory_claiming": faction.n09_territory_claiming,
            "n10_base_structure": faction.n10_base_structure,
            "n11_base_origin": faction.n11_base_origin,
            "n12_base_purpose": faction.n12_base_purpose,
            "n13_long_term_goals": faction.n13_long_term_goals,
            "n14_short_term_goals": faction.n14_short_term_goals,
            "n15_motivations": faction.n15_motivations,
            "n16_goal_strategy": faction.n16_goal_strategy,
            "n17_leader_view_of_pcs": faction.n17_leader_view_of_pcs,
            "n18_contact_with_pcs": faction.n18_contact_with_pcs,
            "n19_possible_developments": faction.n19_possible_developments,
            "n20_faction_theme": faction.n20_faction_theme,
            "creature_names": [x.name for x in faction.creature_ids] if faction.creature_ids else None
        } for faction in factions]

        faction_childs_parents = [{
            'name': faction.name,
            'parent_name': faction.parent_id.name if faction.parent_id else None,
            'child_names': [x.name for x in faction.child_ids] if faction.child_ids else None,
        } for faction in factions]

        dat_str = (f'faction_dikts = {faction_list}\n'
                   f'parent_dikts = {faction_childs_parents}')
        return dat_str

    def _popolate_by_py(self, modulo):
        # Restituisci il dizionario dal modulo
        faction_dikts = getattr(modulo, 'faction_dikts', None)
        parent_dikts = getattr(modulo, 'parent_dikts', None)
        if faction_dikts is None:
            raise ValueError(f"'factions' not found in {name_file}")
        if parent_dikts is None:
            raise ValueError(f"'faction_childs_parents' not found in {name_file}")

        MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}

        # Process each encounter
        for faction in faction_dikts:
            if faction['creature_names']:
                faction['creature_ids'] = [MAP_CREATURE_ID.get(x) for x in faction['creature_names']]
            faction.pop('creature_names', None)
        factions = self.create(faction_dikts)

        for parent_info in parent_dikts:
            if parent_info.get('child_names'):
                child_records = self.env['faction.faction'].search([('name', 'in', parent_info['child_names'])])
                parent_info['child_ids'] = [(6, 0, child_records.ids)] if child_records else []

            if parent_info.get('parent_name'):
                parent_record = self.env['faction.faction'].search([('name', '=', parent_info['parent_name'])])
                parent_info['parent_id'] = parent_record.id if parent_record else None

            faction_record = factions.filtered(lambda x: x.name == parent_info['name'])
            if faction_record:
                faction_record.write({
                    'parent_id': parent_info.get('parent_id', []),
                    'child_ids': parent_info.get('child_ids', []),
                })
