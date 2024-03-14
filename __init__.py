from . import controllers
from . import models
from .utility.costant import BORDERS_MAP


def post_init_hook_hex_map(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per settare:
        - I confini dei Quadranti,
        - I confini interni degli Esagoni
        - I confini esterni degli Esagoni
        - La lista degli Esagoni mancanti
        - La lista degli Esagoni esterni
    """
    hex_macro = env.ref('cf_hex_map.hex_macro_1')
    hex_macro.set_quads_borders()
    A_debug = [quad.set_hexs_borders() for quad in hex_macro.quad_ids]
    B_debug = [quad.set_hexs_external_borders() for quad in hex_macro.quad_ids]
    C_debug = [quad.set_missing_ids() for quad in hex_macro.quad_ids]

    # SCOMMENTARE PER DEBUG
    # with open('.\custom\cf_hex_map\log\set_hexs_borders.txt', 'w') as file:
    #     file.write(''.join(A_debug))
    # # with open('.\custom\cf_hex_map\log\set_missing_ids.txt', 'w') as file:
    # #   file.write(''.join(C_debug))
    # with open('.\custom\cf_hex_map\log\set_hexs_external_borders.txt', 'w') as file:
    #     file.write(''.join(B_debug))
