from . import models


def post_init_hook_cf_hex_biome(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per settare:
        - Le strutture dentro i biomi,
    """
    Structure = env["structure.structure"]
    Structure.popolate_structure_biome()
