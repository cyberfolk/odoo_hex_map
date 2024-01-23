import json
import logging

from odoo.http import request

from odoo import http

_logger = logging.getLogger(__name__)


class HexMapController(http.Controller):

    @http.route("/api/hex_macro", type='http', auth='public', cors='*', csrf=False, save_session=False)
    def fetch_hex_macro(self, **data):
        """End point che ritorna in formato json l' hex_macro, gli hex_quad e gli hex_hex opportunamente incapsulati."""

        _logger.info("RUN fetch_hex_macro")
        hex_macro = request.env.ref('cf_hex_map.hex_macro_1').sudo()
        hex_macro_json = self.obj_odoo_to_json(hex_macro)
        return http.Response(hex_macro_json, content_type='application/json', status=200)

    def obj_odoo_to_json(self, obj_odoo):
        """Metodo di validità generica che trasforma un oggetto di odoo in un json."""
        # read() ritorna un dizionario da un oggetto di odoo.
        obj_dict = obj_odoo.read()[0]  # Uso [0] perché assumo che obj_odoo sia singolo.
        self.filter_metadata(obj_dict)
        obj_expand = self.expand(obj_dict, obj_odoo)  # espando i campi che finiscono con '_id' o '_ids'
        obj_json = json.dumps(obj_expand)
        return obj_json

    def expand(self, obj_dict, obj_odoo):
        """Funzione ricorsiva che espande i campi che finiscono con '_id' o '_ids'. """

        for field_name in obj_dict.keys():
            if field_name.endswith('_id'):
                obj_dict[field_name] = obj_dict[field_name][0]
            if field_name.endswith('_ids'):  # Assumo che ogni campo che finisce per '_ids' corrisponda a una lista id.
                dict_ids = obj_odoo[field_name].read()
                obj_dict[field_name] = [self.filter_metadata(dict_id) for dict_id in dict_ids]
                # Qui parte la ricorsione per espandere correttamente anche sotto-campi del campo appena espanso
                for item_dict, item_odoo in zip(obj_dict[field_name], obj_odoo[field_name]):
                    self.expand(item_dict, item_odoo)
        return obj_dict

    @staticmethod
    def filter_metadata(dikt):
        dikt.pop('__last_update', None)
        dikt.pop('write_date', None)
        dikt.pop('write_uid', None)
        dikt.pop('create_date', None)
        dikt.pop('create_uid', None)
        dikt.pop('display_name', None)
        dikt.pop('hex_list', None)
        return dikt
