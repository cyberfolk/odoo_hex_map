from . import controllers
from . import models
from .utility.costant import BORDERS_MAP


def post_init_hook_hex_map(env):
    """Metodo che vine eseguito successivamente all'installazione modulo per settare i parametri finali
    Come per esempio i Confini dei Quadranti e degli Esagoni"""
    hex_macro = env.ref('cf_hex_map.hex_macro_1')
    hex_macro.set_quads_borders()
