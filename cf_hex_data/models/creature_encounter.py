import csv
import logging
from pathlib import Path

from odoo import fields, Command
from odoo import models

_logger = logging.getLogger(__name__)

# Dizionario per creare degli scontri a SML X con solo creature di CR Y
# Nella tupla sono riportate la quantity di creature di quel CR per ottenere quel SML
# "SML": ("q_cr0125", "q_cr025", "q_cr05", "q_cr1", "q_cr2", "q_cr3", "q_cr4, "q_cr5", "q_cr6", "q_cr7", "q_cr8")
LIST_CR = [0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]
MAP_SML_QTY = {
    "3": (16, 11, 7, 4, None, None, None, 1, None, None, None),
    "4": (20, 14, 9, 5, 3, 2, None, None, 1, None, None),
    "5": (45, 22, 14, 9, 5, 3, None, None, None, None, None),
    "6": (56, 28, 15, 10, 6, 4, None, 2, None, None, None),
    "7": (68, 33, 17, 11, None, 5, 3, None, 2, None, None),
    "8": (84, 42, 21, 14, 8, 6, 4, None, None, None, None),
    "9": (96, 48, 24, 15, 9, None, None, 3, None, None, None),
    "10": (120, 56, 28, 15, 10, 7, 5, None, None, None, 2),
}


class CreatureEncounter(models.Model):
    _name = "creature.encounter"
    _inherit = ['creature.encounter', 'mixin.import.py']

    def _popolate_by_py(self, modulo):
        """Ereditato dal Mixin. Crea record partendo dal modulo '.py'."""
        encounter_dikts = getattr(modulo, 'encounter_dikts', None)
        if encounter_dikts is None:
            raise ValueError(f"'encounter_dikts' not found in {name_file}")

        MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}

        # Ciclo gli scontri per sostituire 'creature_name' con 'creature_id' e 'faction_name' con 'faction_id'
        for encounter in encounter_dikts:
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
        self.create(encounter_dikts)

    def get_data_str(self):
        """Ereditato dal Mixin. Ritorna una stringa di dati da salvare nel file '.py'."""
        encounters = self.search([])
        encounter_list = [{
            "faction_name": encounter.faction_id.name or None,
            "line_ids": [(0, 0, {
                'creature_qty': line.creature_qty,
                'creature_name': line.creature_id.name
            }) for line in encounter.line_ids]
        } for encounter in encounters]
        data_str = f'encounter_dikts = {encounter_list}'
        return data_str


# region METODI DEPRECATI ------------------------------------------------------------------------------------------
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


def popolate_endemic_encounter(self):
    """Crea scontri per le creature con il tag endemico usando la tabella MAP_SML_QTY."""

    _logger.info("DEPRECATE download_encounters_py")
    pass

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
# endregion METODI DEPRECATI ---------------------------------------------------------------------------------------
