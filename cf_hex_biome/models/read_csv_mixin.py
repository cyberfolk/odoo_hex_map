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
    "biome.type": "Tipo di Bioma (biome.type).csv",
    "creature.type": "Tipi di creature (creature.type).csv",
    "creature.tag": "Tag per creature (creature.tag).csv",
    "creature.creature": "Creatura (creature.creature).csv",
    "structure.structure": "Struttura (structure.structure).csv"
}


class ReadCsvMixin(models.AbstractModel):
    _name = 'read.csv.mixin'
    _description = 'Mixin per leggere file csv e popolare modelli'

    def cf_to_odoo_dict(self, row, utility_maps=None):
        """TO OVERRIDE - Traduce una riga di un file csv in un dizionario 'odoo_dict'.
           Ovvero un dizionario adatto a creare record del modello che eredita il mixin."""
        vals = {
            "name": row.get('Nome'),
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
                dicts = self.read_dicts_from_csv(reader)
                for i, dikt in enumerate(dicts):
                    count = f"({str(i + 1).zfill(3)})"
                    if not dikt.get('Nome'):
                        _logger.warning(f" - {count} SKIP   -> Missing 'Nome' field.")
                        continue

                    already_exists = self.search_count([('name', '=', dikt.get('Nome'))]) > 0
                    if already_exists:
                        _logger.info(f" - {count} SKIP   {dikt.get('Nome')} -> Already exists.")
                        continue

                    vals = self.cf_to_odoo_dict(dikt, utility_maps)
                    self.create(vals)
                    _logger.info(f" - {count} CREATE {dikt.get('Nome')}")

                stop = 0
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

    def read_dicts_from_csv(self, reader):
        """Processa le righe di un file CSV per ritornare una lista di dizionari normalizzati in base al campo 'Nome'.

        Il metodo esegue le seguenti operazioni:
        1. FASE 1 [CONTAINER_B]: Raggruppa le righe del CSV in base al campo 'Nome'.
           Ogni volta che il campo 'Nome' cambia, inizia un nuovo batch di righe.
        2. FASE 1 [CONTAINER_D]: Trasforma i batch di righe in dizionari normalizzati, cioè un dizionario con degli
           appositi campi-lista per raggruppare i valori dei campi presenti su più righe dello stesso batch.

        Esempio:
            FILE CSV:
                "Nome", "A", "B", "C", "D"
                "nom1", "a",  "",  "", "b"
                "nom2", "1", "2", "3", "4"
                    "", "a",  "", "c",  ""
                    "",  "", "d", "e",  ""
                "nom3", "1",  "", "1", "1"
                    "",  "", "2",  "",  ""
                    "", "3",  "",  "", "3"
                    "", "4",  "", "4",  ""

            CONTAINER_B:
                [[
                    {'Nome': 'nom1', 'A': 'a', 'B': '', 'C': '', 'D': 'b'}
                ],[
                    {'Nome': 'nom2', 'A': '1', 'B': '2', 'C': '3', 'D': '4'},
                    {'Nome': '', 'A': 'a', 'B': '', 'C': 'c', 'D': ''},
                    {'Nome': '', 'A': '', 'B': 'd', 'C': 'e', 'D': ''}
                ],[
                    {'Nome': 'nom3', 'A': '1', 'B': '', 'C': '1', 'D': '1'},
                    {'Nome': '', 'A': '', 'B': '2', 'C': '', 'D': ''},
                    {'Nome': '', 'A': '3', 'B': '', 'C': '', 'D': '3'},
                    {'Nome': '', 'A': '4', 'B': '', 'C': '4', 'D': ''}
                ]]

            CONTAINER_D:
                 [{'Nome': 'nom1', 'A': 'a', 'B': [], 'C': [], 'D': 'b'},
                  {'Nome': 'nom2', 'A': ['1', 'a'], 'B': ['2', 'd'], 'C': ['3', 'c', 'e'], 'D': '4'},
                  {'Nome': 'nom3''A': ['1', '3', '4'], 'B': '2', 'C': ['1', '4'], 'D': ['1', '3']}]
        """
        list_fields = [v.args.get('string') for k, v in self._fields.items() if v.type in ['one2many', 'many2many']]

        # FASE 1: Raggruppa le righe in base al campo 'Nome'
        container_B = []  # Contenitore di Batch
        batch = []  # Batch che raggruppale le righe del reader inerenti allo stesso campo 'Nome'
        for row in reader:
            if row['Nome']:  # Quando il campo 'Nome' non è vuoto
                if batch:
                    container_B.append(batch)  # Aggiungi il batch precedente al container_B
                batch = [row]  # Inizia un nuovo batch
            else:
                batch.append(row)  # Aggiungi la row al batch corrente
        if batch:  # Aggiungi l'ultimo gruppo se esiste
            container_B.append(batch)

        # FASE 2: Trasforma i batch di righe in dizionari normalizzati
        container_D = []  # Contenitore di Dizionari da ritornare
        dikt = {}  # Dizionario da ritornare
        for batch in container_B:
            dikt = {}
            for row in batch:
                for key, value in row.items():
                    dikt.setdefault(key, []).append(value)
            for key, value in dikt.items():
                value = list(filter(lambda x: x, value))  # Filtra valori vuoti
                dikt[key] = value
                if key not in list_fields:
                    dikt[key] = value[0] if value else None
            container_D.append(dikt)

        return container_D
