import importlib.util
import logging
import os
from pathlib import Path

from odoo import models

_logger = logging.getLogger(__name__)

MAP_MODEL_PY = {
    "creature.encounter": "encounters.py",
    "faction.faction": "factions.py"
}


class MixinImportPy(models.AbstractModel):
    _name = 'mixin.import.py'
    _description = 'Mixin per popolare i vari modelli da python'

    def _get_file_path(self):
        """Helper method to get the file path based on the model name."""
        nome_file = MAP_MODEL_PY.get(self._name)
        if not nome_file:
            raise ValueError(f"No file mapping found for model {self._name}")
        return (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

    def download_data_py(self):
        """Scarica i dati del modello in un file '.py' mettendolo nella cartella 'data'."""
        _logger.info(f"START download_data_py ({self._name})")

        data_str = self.get_data_str()
        file_path = self._get_file_path()

        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data_str)
        except IOError as e:
            _logger.error(f"Failed to write to {file_path}: {e}")
        finally:
            _logger.info(f"END download_data_py ({self._name})")

    def popolate_by_py(self):
        """Crea record partendo dal file '.py' nella cartella 'data'."""
        _logger.info(f"** START ** popolate_by_py() - ({self._name})")
        try:
            file_path = self._get_file_path()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            spec = importlib.util.spec_from_file_location(Path(file_path).stem, file_path)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            self._popolate_by_py(modulo)

        except FileNotFoundError as e:
            _logger.error(f"** ERROR ** File not found: {e}")
        except Exception as e:
            _logger.error(f"** ERROR ** popolate_by_py() - ({self._name})")
            _logger.exception(e)
        finally:
            _logger.info(f"** END   ** popolate_by_py() - ({self._name})")

    def _popolate_by_py(self, modulo):
        """Da ereditare nei modelli che implementano il mixin."""
        pass

    def get_data_str(self):
        """Da ereditare nei modelli che implementano il mixin."""
        pass
