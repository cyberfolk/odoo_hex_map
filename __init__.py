from . import controllers
from . import models
from .utility.costant import BORDERS_MAP


def post_init_hook_hex_map(env):
    """Metodo che vine eseguito dopo l'installazione del modulo. Serve per settare:
        - I confini dei Quadranti,
        - I confini interni degli Esagoni
        - I confini esterni degli esagoni
    """
    hex_macro = env.ref('cf_hex_map.hex_macro_1')
    hex_macro.set_quads_borders()
    [quad.set_hexs_borders() for quad in hex_macro.quad_ids]
    [quad.set_hexs_external_borders() for quad in hex_macro.quad_ids]
