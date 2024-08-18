import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _name = "creature.creature"
    _inherit = 'read.csv.mixin'
    _description = "Creatura"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome generico della creatura per come è registrata sui manuali."
    )

    cr = fields.Float(
        string="Grado Sfida",
        required=True,
        help="Grado sfida della creatura."
    )

    link_5et = fields.Char(
        string="link 5et",
        help="Link al form della creatura su 5etools per avere maggiori dettagli."
    )

    skip = fields.Boolean(
        string="Sconosciuta",
        help="Se selezionato, la creatura è sconosciuta dalla maggior parte dei DM. Considera creature più note."
    )

    cool = fields.Boolean(
        string="Interessante",
        help="Se selezionato, la creatura è molto interessante, e funziona bene per creare atmosfera."
    )

    tag_ids = fields.Many2many(
        comodel_name="creature.tag",
        string="Tag",
        help="Tag della creatura"
    )

    type_id = fields.Many2one(
        comodel_name="creature.type",
        string="Tipo",
        help="Tipo di creatura"
    )

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""
        MAP_TYPES_IDS, MAP_TAGS_IDS = utility_maps[0], utility_maps[1]

        tag_field_list = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
        tag_list = [row.get(tag) for tag in tag_field_list]
        tag_ids_list = [MAP_TAGS_IDS[tag] for tag in tag_list if tag]
        vals = {
            'skip': bool(row.get('skip')),
            'cool': bool(row.get('cool')),
            'type_id': MAP_TYPES_IDS[row.get('type')],
            'tag_ids': [(6, 0, tag_ids_list)],
            'name': row.get('name'),
            'link_5et': row.get('link'),
            'cr': float(row.get('cr').replace(',', '.')) or 0,
        }
        return vals
