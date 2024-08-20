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
        string="Link 5et",
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

    biome_high_prob_ids = fields.Many2many(
        comodel_name="biome.type",
        relation="creature_biome_high_prob_rel",  # Specify a unique relation name
        string="Biomi %Alta",
        help="Biomi con Alta probabilità di trovare la creatura."
    )

    biome_low_prob_ids = fields.Many2many(
        comodel_name="biome.type",
        relation="creature_biome_low_prob_rel",  # Specify a unique relation name
        string="Biomi %Bassa",
        help="Biomi con Bassa probabilità di trovare la creatura."
    )

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""

        MAP_TYPES_IDS, MAP_TAGS_IDS, MAP_BIOME_IDS = utility_maps
        biome_high_prob_ids = [MAP_BIOME_IDS[bioma] for bioma in row.get('Biomi %Alta')]
        biome_low_prob_ids = [MAP_BIOME_IDS[bioma] for bioma in row.get('Biomi %Bassa')]
        tag_ids_list = [MAP_TAGS_IDS[tag] for tag in row.get('Tag')]

        vals = {
            'skip': bool(row.get('Sconosciuta')),
            'cool': bool(row.get('Interessante')),
            'type_id': MAP_TYPES_IDS[row.get('Tipo')],
            'tag_ids': [(6, 0, tag_ids_list)],
            'name': row.get('Nome'),
            'link_5et': row.get('Link 5et'),
            'cr': float(row.get('Grado Sfida')) or 0,
            'biome_high_prob_ids': [(6, 0, biome_high_prob_ids)],
            'biome_low_prob_ids': [(6, 0, biome_low_prob_ids)],
        }
        return vals
