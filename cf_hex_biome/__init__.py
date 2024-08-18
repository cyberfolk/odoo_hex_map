from . import models


def post_init_hook_cf_hex_biome(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per settare:
        - I Tipi di Biomi,
        - Le strutture dentro i biomi,
        - I Tag delle creature,
        - I Tipi delle creature,
        - Le Creature,
    """
    # env["biome.type"].popolate_by_csv()
    # env["structure.structure"].popolate_by_csv()
    # env["creature.tag"].popolate_by_csv()
    # env["creature.type"].popolate_by_csv()
    # env["creature.creature"].popolate_by_csv()
