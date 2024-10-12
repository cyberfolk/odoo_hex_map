from . import controllers
from . import models
from .utility.constant import BORDERS_MAP


def post_init_hook_cf_hex_base(env):
    env["hex.macro"].create([{"name": "Macro Area 01"}])