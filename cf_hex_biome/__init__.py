from . import models


def post_init_hook_cf_hex_biome(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per settare:
        - Le strutture dentro i biomi,
        - I Tag delle creature,
        - I Tipi delle creature,
        - Le Creature,
    """
    Structure = env["structure.structure"]
    Structure.popolate_structure_biome()
    CreatureTag = env["creature.tag"]
    CreatureTag.popolate_creature_tag()
    CreatureType = env["creature.type"]
    CreatureType.popolate_creature_type()
    Creature = env["creature.creature"]
    Creature.popolate_creature()
