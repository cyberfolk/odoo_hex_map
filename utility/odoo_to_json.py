# Tool di Validità generale
import json


def obj_odoo_to_json(obj_odoo):
    """ Trasforma un oggetto di odoo in un json.
        :param obj_odoo: Può essere sia un oggetto singolo che una lista di oggetti.
        :return: Un JSON, o una lista di JSON."""
    if len(obj_odoo) > 1:
        dict_obj = [process_obj(obj) for obj in obj_odoo]
    else:
        dict_obj = process_obj(obj_odoo)
    obj_json = json.dumps(dict_obj)
    return obj_json


def process_obj(obj):
    """Riceve un oggetto di Odoo e lo trasforma in un dizionario."""
    # read() ritorna un dizionario da un oggetto di odoo.
    obj_dict = obj.read()[0]  # Uso [0] perché assumo che obj_odoo sia singolo.
    filter_metadata(obj_dict)
    obj_expand = expand(obj_dict, obj)  # espando i campi che finiscono con '_id' o '_ids'
    return obj_expand


def expand(obj_dict, obj_odoo):
    """Funzione ricorsiva che espande i campi che finiscono con '_id' o '_ids'. """
    for field_name in obj_dict.keys():
        if field_name.endswith('_id'):
            obj_dict[field_name] = obj_dict[field_name][0]
        if field_name.endswith('_ids'):  # Assumo che ogni campo che finisce per '_ids' corrisponda a una lista id.
            dict_ids = obj_odoo[field_name].read()
            obj_dict[field_name] = [filter_metadata(dict_id) for dict_id in dict_ids]
            # Qui parte la ricorsione per espandere correttamente anche i sotto-campi del campo appena espanso
            for item_dict, item_odoo in zip(obj_dict[field_name], obj_odoo[field_name]):
                expand(item_dict, item_odoo)
    return obj_dict


def filter_metadata(dikt):
    dikt.pop('__last_update', None)
    dikt.pop('write_date', None)
    dikt.pop('write_uid', None)
    dikt.pop('create_date', None)
    dikt.pop('create_uid', None)
    dikt.pop('display_name', None)
    dikt.pop('hex_list', None)
    dikt.pop('tmp', None)
    return dikt
