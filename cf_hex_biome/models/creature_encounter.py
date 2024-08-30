import csv
import importlib.util
import logging
import os
from pathlib import Path

from odoo import fields, api, Command
from odoo import models
from ..utility.exp import MAP_QTY_MOD, MAP_LEVEL_EXP, MAP_SML_QTY, LIST_CR

_logger = logging.getLogger(__name__)


class CreatureEncounter(models.Model):
    _name = "creature.encounter"
    _inherit = 'read.csv.mixin'
    _description = "Scontro"

    name = fields.Char(
        string="Nome",
        help="Nome dello scontro.",
        compute="_compute_name",
        store=True
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

    sml = fields.Integer(
        string="SML",
        compute="_compute_sml",
        help="Scontro Mortale per 4 PG di Livello 'SML'",
        store=True,
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        compute="_compute_creature_ids",
        string="Creature",
        help="Creature che compongono lo scontro.",
    )

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_encounter_biome_biome_rel",
        compute="_compute_biome_ids",
        string="Biomi",
        help="Biomi dove può verificarsi lo scontro.",
        store=True,
    )

    is_endemic = fields.Boolean(
        string="Endemico",
        compute="_compute_is_endemic",
        store=True,
    )

    faction_id = fields.Many2one(
        comodel_name="faction.faction",
        string="Fazione",
        help="Fazione dello scontro",
    )

    @api.depends("line_ids", "faction_id")
    def _compute_is_endemic(self):
        for record in self:
            record.is_endemic = all(line.is_endemic for line in record.line_ids)
            if record.faction_id:
                record.is_endemic = False

    @api.depends("line_ids", "faction_id")
    def _compute_name(self):
        for record in self:
            record.name = " + ".join(filter(None, record.line_ids.mapped("name")))
            if record.faction_id:
                record.name = f"{record.faction_id.name}: {record.name}"
            elif record.is_endemic:
                record.name = f"Endemico: {record.name}"
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
            modificatore = MAP_QTY_MOD.get(str(record.tot_creatures), 4)
            record.exp_adj = record.exp_sum * modificatore
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
    def _compute_biome_ids(self):
        for record in self:
            if record.creature_ids and record.creature_ids.biome_ids:
                record.biome_ids = record.creature_ids.biome_ids
            if not record.biome_ids:
                record.biome_ids = []  # or any other default value or action

    def popolate_endemic_encounter(self):
        _logger.info("START popolate_endemic_encounter")
        for sml, qtys in MAP_SML_QTY.items():
            _logger.info(f"** START SML {sml}")
            for i, qty in enumerate(qtys):
                if not qty or qty > 11:
                    continue
                cr = LIST_CR[i]
                creatures = self.env["creature.creature"].search([("cr", "=", cr), ("is_endemic", "=", True)])
                _logger.info(f"**** START SML {sml} - CR {cr} - FIND {len(creatures)} CREATURES")
                for n, creature in enumerate(creatures):
                    encounter = self.search([("name", "=", f"Endemico: {qty} x {creature.name}")])
                    if encounter:
                        _logger.warning(f"*** ({n + 1}/{len(creatures)}) SKIP {encounter.name} - ALREADY EXISTS")
                        continue
                    encounter = self.create({
                        "line_ids": [Command.create({
                            'creature_qty': qty,
                            'creature_id': creature.id
                        })]
                    })
                    _logger.info(f"****** ({n + 1}/{len(creatures)}) CREATE {encounter.name}")
                _logger.info(f"**** END SML {sml} - CR {cr}")
            _logger.info(f"** END SML {sml}")
        _logger.info("END popolate_endemic_encounter")

    def popolate_by_py(self):
        """Crea record partendo dal encounter.py che deve essere presente nella cartella 'data'."""
        _logger.info(f"** START ** popolate_by_py() - ({self._name})")
        try:
            name_file = 'encounters.py'
            file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file).as_posix()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            spec = importlib.util.spec_from_file_location("encounters", file_path)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            # Restituisci il dizionario dal modulo
            encounters = getattr(modulo, 'encounters', None)
            if encounters is None:
                raise ValueError(f"'encounters' not found in {name_file}")

            MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}

            # Process each encounter
            for encounter in encounters:
                # Map creature names to IDs in line items
                for line in encounter['line_ids']:
                    creature_name = line[2].pop('creature_name', None)
                    if creature_name:
                        line[2]['creature_id'] = MAP_CREATURE_ID.get(creature_name)
                        if not line[2]['creature_id']:
                            raise ValueError(f"Creature '{creature_name}' not found")

                # Map faction name to faction ID
                faction_name = encounter.pop('faction_name', None)
                if faction_name:
                    faction = self.env['faction.faction'].search([('name', '=', faction_name)], limit=1)
                    if not faction:
                        raise ValueError(f"Faction '{faction_name}' not found")
                    encounter['faction_id'] = faction.id

            # Crea i record
            self.create(encounters)

        except Exception as e:
            _logger.error(f"** ERROR ** popolate_by_py() - ({self._name})")
            _logger.exception(e)
        _logger.info(f"** END  ** popolate_by_py() - ({self._name})")

    # region --------- DEPRECATI ---------------------------------------------------------------------------------------
    def download_encounters_py(self):
        _logger.info("DEPRECATE download_encounters_py")
        pass
        """Scarica i dati degli incontri nel file 'encounters.py' mettendolo nella cartella 'data'."""
        _logger.info("START download_encounters_py")

        # Fetch encounters and structure the data
        encounters = self.search([])
        encounters_list = [{
            "faction_name": encounter.faction_id.name or None,
            "line_ids": [
                {
                    'creature_qty': line.creature_qty,
                    'creature_name': line.creature_id.name
                } for line in encounter.line_ids
            ]
        } for encounter in encounters]

        nome_file = 'encounters.py'
        contenuto = f'encounters = {encounters_list}'
        file_path = (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

        try:
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            _logger.info("END download_encounters_py - SUCCESS")
        except IOError as e:
            _logger.error(f"Failed to write to {file_path}: {e}")

    def popolate_faction_encounter(self):
        """Crea record partendo dal faction_encounter che deve essere presente nella cartella 'data'."""

        _logger.info("DEPRECATE popolate_faction_encounter")
        pass

        MAP_FACTION_ID = {x.name: x.id for x in self.env['faction.faction'].search([])}
        MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}
        name_file_csv = 'faction_encounter.csv'
        file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file_csv).as_posix()
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            i = 0
            for row in reader:
                i += 1
                faction_id = MAP_FACTION_ID.get(row['fazione'])
                list_creature_name = [row['c1'], row['c2'], row['c3'], row['c4']]
                list_creature_id = [MAP_CREATURE_ID[x] for x in list_creature_name if x]
                list_creature_number = [int(row['n1'] or 0), int(row['n2'] or 0), int(row['n3'] or 0),
                                        int(row['n4'] or 0)]

                lines = []
                for _id, num in zip(list_creature_id, list_creature_number):
                    if (_id is None) != (num is None):
                        raise ValueError("Un elemento è `None` mentre l'altro è valorizzato.")
                    if _id is not None and num is not None:
                        lines.append({
                            'creature_qty': num,
                            'creature_id': _id
                        })

                encounter = self.create({
                    "faction_id": faction_id,
                    "line_ids": [(fields.Command.create(line)) for line in lines]
                })
                print(f"{i} - {encounter.name} - {row['fazione']} - {list_creature_name} - {list_creature_number}")
    # region --------- DEPRECATI ---------------------------------------------------------------------------------------

