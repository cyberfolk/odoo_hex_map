# read.csv.mixin è una classe mixin per facilitare il processo di lettura del file csv e annessa creazione di record.
# Il metodo principale del mixin è popolate_by_csv.
# I modelli che implementano questo mixin devono estendere il metodo cf_to_odoo_dict()
# metodo con il quale si converte una riga del file csv in un dizionario di odoo
import csv
import inspect
import logging
import os
from pathlib import Path

from odoo import models

_logger = logging.getLogger(__name__)

MAP_MODEL_CSV = {
    "biome.type": "biome_type.csv",
    "creature.type": "creature_type.csv",
    "creature.tag": "creature_tag.csv",
    "creature.creature": "creature_creature.csv",
    "structure.structure": "structure_structure.csv"
}


class ReadCsvMixin(models.AbstractModel):
    _name = 'read.csv.mixin'
    _description = 'Mixin per leggere file csv e popolare modelli'

    def cf_to_odoo_dict(self, row, utility_maps=None):
        """TO OVERRIDE - Traduce una riga di un file csv in un dizionario 'odoo_dict'.
           Ovvero un dizionario adatto a creare record del modello che eredita il mixin."""
        vals = {
            "name": row.get('name'),
        }
        return vals

    def popolate_by_csv(self):
        """Crea record partendo da un file CSV che deve essere presente nella cartella 'data'.

        Il metodo esegue le seguenti operazioni:
        1. Recupera il nome del file CSV associato al modello attuale tramite il dizionario `MAP_MODEL_CSV`.
        2. Costruisce il percorso completo del file CSV e verifica se il file esiste.
        3. Apre il file CSV e legge i dati riga per riga.
        4. Per ogni riga, verifica la presenza del campo 'name'. Se mancante, emette un avviso e salta la riga.
        5. Controlla se esiste già nel DB un record con lo stesso 'name' della riga corrente. Se esiste si salta la riga.
        6. Se il record non esiste, converte i dati della riga in un dizionario e crea il nuovo record.
        7. In caso di errore durante, registra un messaggio di errore e crea un record di log nel database Odoo.

        - Il file CSV deve essere presente nella sotto-cartella 'data' del progetto.
        - `MAP_MODEL_CSV` deve essere configurato correttamente per associare i nomi dei modelli ai rispettivi file CSV.
        """

        # Creo delle mappe di conversione {nome: id}
        map_creature_types_ids = {x.name: x.id for x in self.env['creature.type'].search([])}
        map_creature_tags_ids = {x.name: x.id for x in self.env['creature.tag'].search([])}
        map_biome_types_ids = {x.name: x.id for x in self.env['biome.type'].search([])}
        utility_maps = (map_creature_types_ids, map_creature_tags_ids, map_biome_types_ids)

        _logger.info(f"** START ** popolate_by_csv() - ({self._name})")
        try:
            # Recupero il path del file CSV
            name_file_csv = MAP_MODEL_CSV.get(self._name)
            if not name_file_csv:
                _logger.error(f"No CSV file mapped for model: {self._name}")
                return

            file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file_csv).as_posix()
            if not os.path.exists(file_path):
                _logger.error(f"File not found: {file_path}")
                return

            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    count = f"({str(i + 1).zfill(3)})"
                    if not row.get('name'):
                        _logger.warning(f" - {count} SKIP   -> Missing 'name' field.")
                        continue

                    already_exists = self.search_count([('name', '=', row.get('name'))]) > 0
                    if already_exists:
                        _logger.info(f" - {count} SKIP   {row.get('name')} -> Already exists.")
                        continue

                    vals = self.cf_to_odoo_dict(row, utility_maps)
                    self.create(vals)
                    _logger.info(f" - {count} CREATE {row.get('name')}")

        except Exception as e:
            msg = f"Errore durante la lettura del file csv:\n {e}"
            _logger.error(msg)
            frame = inspect.currentframe()
            self.env['ir.logging'].sudo().create({
                'name': self._name,
                'type': 'server',
                'level': 'ERROR',
                'path': frame.f_code.co_filename,
                'line': frame.f_lineno,
                'dbname': self.env.cr.dbname,
                'message': msg,
                'func': 'popolate_by_csv',
            })
        _logger.info(f"** END  ** popolate_by_csv() - ({self._name})")
