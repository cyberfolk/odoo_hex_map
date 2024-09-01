import logging

from . import models
from . import controllers

_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


def post_init_hook_cf_hex_biome(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per popolare:
        - I Biomi,
        - Le strutture dentro i biomi,
        - I Tag delle creature,
        - I Tipi delle creature,
        - Le Creature,
        - Gli scontri,
    """
    try:
        env["biome.biome"].popolate_by_csv()
        env["structure.structure"].popolate_by_csv()
        env["creature.tag"].popolate_by_csv()
        env["creature.type"].popolate_by_csv()
        env["creature.creature"].popolate_by_csv()
        env["faction.faction"].popolate_by_py()
        env["creature.encounter"].popolate_by_py()
    except Exception as e:
        msg = (f"Errore nella funzione post_init_hook_cf_hex_biome()\n"
               f"Fallito caricamento dei dati per il modulo cf_hex_biome\n"
               f"{e}")
        raise ValidationError(msg)
