import logging

from odoo.exceptions import ValidationError

from . import models

_logger = logging.getLogger(__name__)


def post_init_hook_cf_hex_data(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per popolare:
         - I biomi,
         - Le Strutture
         - I Tag delle Creature,
         - I Tipi delle Creature,
         - Le Creature,
         - Le Fazioni,
         - Gli Scontri
    """
    try:
        _logger.info("* START * post_init_hook_cf_hex_data()")
        env["biome.biome"].popolate_by_csv()
        env["structure.structure"].popolate_by_csv()
        env["creature.tag"].popolate_by_csv()
        env["creature.type"].popolate_by_csv()
        env["creature.creature"].popolate_by_csv()
        env["faction.faction"].popolate_by_py()
        env["creature.encounter"].popolate_by_py()
    except Exception as e:
        msg = (f"Errore nella funzione post_init_hook_cf_hex_data()\n"
               f"Fallito caricamento dei dati per il modulo cf_hex_biome\n"
               f"{e}")
        raise ValidationError(msg)
    finally:
        _logger.info("* END   * post_init_hook_cf_hex_data()")
