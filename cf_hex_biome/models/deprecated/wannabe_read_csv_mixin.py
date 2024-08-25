# AL MOMENTO NON è COMPLETATA PER VIA DEI CAMPI SELECTION, MA QUESTO FILE VORREBBE ESSERE UNA VERSIONE
# GENERALIZZATA DEL FILE read_csv_mixin.py senza dover implementare ogni volta cf_to_odoo_dict()
# read.csv.mixin è una classe mixin per record partendo da un file csv
import csv
import inspect
import logging
import os
from pathlib import Path

from odoo import models, Command

_logger = logging.getLogger(__name__)

MAP_MODEL_CSV = {
    "biome.biome": "Bioma (biome.biome).csv",
    "creature.type": "Tipi di creature (creature.type).csv",
    "creature.tag": "Tag per creature (creature.tag).csv",
    "creature.creature": "Creatura (creature.creature).csv",
    "structure.structure": "Struttura (structure.structure).csv"
}


class ReadCsvMixin(models.AbstractModel):
    _name = 'read.csv.mixin'
    _description = 'Mixin per leggere file csv e popolare modelli'

    def popolate_by_csv(self):
        """Crea record partendo da un file CSV che deve essere presente nella cartella 'data'.

        Steps:
        1. Recupera il nome del file CSV associato al modello attuale tramite il dizionario `MAP_MODEL_CSV`.
        2. Costruisce il percorso completo del file CSV e verifica se il file esiste.
        3. Apre il file CSV e invoca la funzione `read_dicts_from_csv` che ritorna una lista di dizionari.
        4. Per ogni riga, verifica la presenza del campo 'Nome'. Se mancante, emette un avviso e salta la riga.
        5. Controlla se esiste già nel DB un record con lo stesso 'Nome' della riga corrente. Se esiste si salta la riga.
        6. Se il record non esiste, converte i dati di dikt in un odoo_dict per creare il nuovo record.
        7. In caso di errore durante, registra un messaggio di errore e crea un record di log nel database Odoo.

        - Il file CSV deve essere presente nella sotto-cartella 'data' del progetto.
        - `MAP_MODEL_CSV` deve essere configurato correttamente per associare i nomi dei modelli ai rispettivi file CSV.
        """
        _logger.info(f"** START ** popolate_by_csv() - ({self._name})")
        try:
            METADATA = self.get_field_metadata()
            # 1. Recupera il nome del file CSV
            name_file_csv = MAP_MODEL_CSV.get(self._name)
            if not name_file_csv:
                _logger.error(f"No CSV file mapped for model: {self._name}")
                raise FileNotFoundError(f"No CSV file mapped for model: {self._name}")

            # 2. Costruisce il percorso completo del file CSV
            file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file_csv).as_posix()
            if not os.path.exists(file_path):
                _logger.error(f"File not found: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")

            # 3. Apre il file CSV e invoca la funzione `read_dicts_from_csv`
            with open(file_path, mode='r', encoding='utf-8') as file:
                dikt = read_dicts_from_csv(file)

                for i, dikt in enumerate(dikt):
                    dikt_name = (dikt.get('Nome') or [None])[0]
                    count = f"({str(i + 1).zfill(3)})"

                    # 4. Verifica la presenza del campo 'Nome'
                    if not dikt_name:
                        _logger.warning(f" - {count} SKIP   -> Missing 'Nome' field.")
                        continue

                    # 5. Controlla se esiste già un record con lo stesso 'Nome'
                    already_exists = self.search_count([('name', '=', dikt_name)]) > 0
                    if already_exists:
                        _logger.info(f" - {count} SKIP   {dikt_name} -> Already exists.")
                        continue

                    # 6. Creo il nuovo record.
                    odoo_dikt = get_odoo_dikt(dikt, METADATA)
                    self.create(odoo_dikt)
                    _logger.info(f" - {count} CREATE {dikt_name}")

        except Exception as e:
            msg = f"** END  ** popolate_by_csv() - Errore durante la lettura del file csv:\n {e}"
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
            raise e
        _logger.info(f"** END  ** popolate_by_csv() - ({self._name})")

    def get_field_metadata(self):
        """Restituisce un dizionario con i metadata dei campi del modello.
        Le chiavi del dizionario sono i nomi(string) dei campi.
        A ogni chiave è associato un dizionario contente:
            - name (str): Il nome tecnico del campo.
            - type (str): Il tipo di campo (es. 'char', 'integer', 'many2one').
            - comodel_name (str): Il nome del modello associato se il campo è di tipo relazionale.
            - comodel_data (dict): Un dizionario che mappa i nomi dei record agli ID per i campi di tipo relazionale.
        """
        field_metadata = {}
        for field_name, field_obj in self._fields.items():
            comodel_data = None
            if field_obj.comodel_name:
                comodel_records = self.env[field_obj.comodel_name].search([])
                comodel_data = {record.name: record.id for record in comodel_records}

            field_metadata[field_obj.string] = {
                'name': field_obj.name,
                'type': field_obj.type,
                'comodel_name': field_obj.comodel_name,
                'comodel_data': comodel_data,
            }
        return field_metadata


def read_dicts_from_csv(csv_file):
    """Processa le righe di un file CSV per ritornare una lista di dizionari normalizzati in base al campo 'Nome'.
    Per prima cosa cicla sulle righe del file csv per raggruppa in batch in base al campo 'Nome',
    una volta identificato un batch lo trasforma in un dizionario normalizzato e lo inserisce in una lista.

    @param csv_file: Un file CSV con formato Odoo-style contenente records del modello che eredita il mixin.
            I file CSV Odoo-style usano più righe dello stesso record per rappresentare i campo O2M e M2M.
    @return: Una lista di dizionari normalizzati, ovvero dizionari che per chiave hanno i nomi delle colonne csv,
            e per valori hanno la lista dei valori che prima erano splittati sulle righe del singolo batch.

    FILE CSV Odoo-style - Le colonne A e B sono campi O2M
                "Nome", "A", "B", "C", "D"
                "nom1", "a",  "", "c",  ""
                "nom2", "1", "2", "c",  ""
                    "", "a",  "",  "",  ""
                    "",  "", "d",  "",  ""

    BATCH:     [[
                    {'Nome': 'nom1', 'A': 'a', 'B':  '', 'C': 'c', 'D': ''}
                ],[
                    {'Nome': 'nom2', 'A': '1', 'B': '2', 'C': 'c', 'D': ''},
                    {'Nome':     '', 'A': 'a', 'B':  '', 'C':  '', 'D': ''},
                    {'Nome':     '', 'A': '',  'B': 'd', 'C':  '', 'D': ''}
                ]]

    RITORNA:    [{'Nome': ['nom1'], 'A': ['a'],      'B': [],         'C': ['c],  'D': ''},
                 {'Nome': ['nom2'], 'A': ['1', 'a'], 'B': ['2', 'd'], 'C': ['c'], 'D': ''}]
    """

    dikt_list = []  # Contenitore di Batch
    batch = []  # Batch che raggruppale le righe del reader inerenti allo stesso campo 'Nome'
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row.get('Nome'):  # Il campo Nome è valorizzato: aggiungo il batch nel dikt_list e ne inizio uno nuovo
            if batch:
                dikt = get_normalized_dikt(batch)
                dikt_list.append(dikt)
            batch = [row]
        else:  # Il campo Nome NON è valorizzato: aggiungo la row al batch corrente
            batch.append(row)
    if batch:  # Aggiungi l'ultimo gruppo se esiste
        dikt = get_normalized_dikt(batch)
        dikt_list.append(dikt)
    return dikt_list


def get_normalized_dikt(_batch):
    _dikt = {}
    for _row in _batch:  # Unifico i batch di righe in un unico dizionario {key: list}
        for key, value in _row.items():
            _dikt.setdefault(key, []).append(value)
    return _dikt


def get_odoo_dikt(dikt, metadata):
    odoo_dikt = {}
    for field, value in dikt.items():
        value = list(filter(lambda x: x, value))  # Filtra le liste eliminando i valori vuoti
        new_name = metadata[field]['name']
        # Se il campo non è 'one2many' o 'many2many' estraggo il valore dall lista
        if metadata[field]['type'] not in ['one2many', 'many2many']:
            value = value[0] if value else None
        if value and metadata[field]['comodel_data']:
            if metadata[field]['type'] in ['one2many', 'many2many']:
                list_ids = [metadata[field]['comodel_data'].get(x) for x in value]
                value = [Command.link(list_ids)]
            if metadata[field]['type'] in ['many2one']:
                value = metadata[field]['comodel_data'][value]
        if value and metadata[field]['type'] == 'integer':
            value = int(value)
        if value and metadata[field]['type'] == 'float':
            value = float(value)
        if value and metadata[field]['type'] == 'boolean':
            value = bool(value)

        odoo_dikt[new_name] = value
    return odoo_dikt
