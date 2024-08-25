import csv
import inspect
import logging
import os
from pathlib import Path

from odoo import models

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
        """Crea record partendo da un file CSV che deve essere presente nella cartella 'data'."""
        _logger.info(f"** START ** popolate_by_csv() - ({self._name})")
        try:
            file_path = self._get_csv_file_path()
            dikt_list = read_dicts_from_csv(file_path)

            for i, dikt in enumerate(dikt_list):
                dikt_name = dikt.get('Nome', [None])[0]
                if not dikt_name or self._record_exists(dikt_name):
                    continue
                odoo_dikt = self._prepare_record_dict(dikt)
                self.create(odoo_dikt)
                _logger.info(f" - ({str(i + 1).zfill(3)}) CREATE {dikt_name}")

        except Exception as e:
            self._log_error(e)
            raise e
        _logger.info(f"** END  ** popolate_by_csv() - ({self._name})")

    def _get_csv_file_path(self):
        """Recupera e verifica il percorso del file CSV associato al modello."""
        name_file_csv = MAP_MODEL_CSV.get(self._name)
        if not name_file_csv:
            raise FileNotFoundError(f"No CSV file mapped for model: {self._name}")
        file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file_csv).as_posix()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path

    def _record_exists(self, dikt_name):
        """Controlla se un record esiste già."""
        return self.search_count([('name', '=', dikt_name)]) > 0

    def _prepare_record_dict(self, dikt):
        """Prepara il dizionario Odoo dal dikt normalizzato."""
        metadata = self.get_field_metadata()
        return get_odoo_dikt(dikt, metadata)

    def _log_error(self, error):
        """Registra un messaggio di errore e crea un record di log nel database."""
        msg = f"** END  ** popolate_by_csv() - Errore durante la lettura del file csv:\n {error}"
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

    def get_field_metadata(self):
        """Restituisce un dizionario con i metadata dei campi del modello."""
        field_metadata = {}
        for field_name, field_obj in self._fields.items():
            field_metadata[field_obj.string] = {
                'name': field_obj.name,
                'type': field_obj.type,
                'comodel_name': field_obj.comodel_name,
                'map_comodel': self._get_comodel_map(field_obj),
                'map_selection': {v: k for k, v in field_obj.selection} if field_obj.type == 'selection' else None
            }
        return field_metadata

    def _get_comodel_map(self, field_obj):
        """Genera una mappa dei nomi dei record agli ID per i campi relazionali."""
        if field_obj.comodel_name:
            return {rec.name: rec.id for rec in self.env[field_obj.comodel_name].search([])}
        return None


def read_dicts_from_csv(file_path):
    """Processa il CSV per ritornare una lista di dizionari normalizzati."""
    dikt_list = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        batch = []
        for row in reader:
            if row.get('Nome'):
                if batch:
                    dikt_list.append(get_normalized_dikt(batch))
                batch = [row]
            else:
                batch.append(row)
        if batch:
            dikt_list.append(get_normalized_dikt(batch))
    return dikt_list


def get_normalized_dikt(batch):
    """Unifica le righe in un dizionario normalizzato."""
    return {key: [v for v in (value or []) if v] for key, value in get_combined_batch(batch).items()}


def get_combined_batch(batch):
    """Combina le righe di un batch."""
    combined = {}
    for row in batch:
        for key, value in row.items():
            combined.setdefault(key, []).append(value)
    return combined


def get_odoo_dikt(normalized_dikt, metadata):
    """Converte il dikt normalizzato in un odoo_dikt."""
    odoo_dikt = {}
    for field, value in normalized_dikt.items():
        if field in metadata:
            field_meta = metadata[field]
            odoo_dikt[field_meta['name']] = convert_value(
                value, field_meta['type'], field_meta.get('map_comodel'), field_meta.get('map_selection')
            )
    return odoo_dikt


def convert_value(value, field_type, map_comodel=None, map_selection=None):
    """Converte il valore in base al tipo di campo."""
    if not value:
        return None
    if field_type in ['many2one', 'one2many', 'many2many']:
        if not map_comodel:
            return None
        if field_type == 'many2one':
            return map_comodel.get(value[0])
        return [(6, 0, [map_comodel.get(x) for x in value])]
    if field_type == 'integer':
        return int(value[0])
    if field_type == 'float':
        return float(value[0])
    if field_type == 'boolean':
        return bool(value[0])
    if field_type == 'selection':
        return map_selection.get(value[0])
    return value[0]
