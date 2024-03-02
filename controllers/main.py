import logging

from odoo.http import request

from odoo import http
from ..utility.odoo_to_json import obj_odoo_to_json

_logger = logging.getLogger(__name__)


class HexMapController(http.Controller):

    @http.route("/api/hex_macro",
                type='http', auth='public', cors='*', csrf=False, methods=['GET'],  save_session=False)
    def fetch_hex_macro(self, **data):
        """End point che ritorna in formato json l' hex_macro, gli hex_quad e gli hex_hex opportunamente incapsulati."""

        _logger.info("RUN fetch_hex_macro")
        hex_macro = request.env.ref('cf_hex_map.hex_macro_1').sudo()
        hex_macro_json = obj_odoo_to_json(hex_macro)
        return http.Response(hex_macro_json, content_type='application/json', status=200)
