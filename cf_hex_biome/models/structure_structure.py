from odoo import fields, models


class StructureStructure(models.Model):
    _name = "structure.structure"
    _inherit = 'read.csv.mixin'
    _description = "Struttura"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Struttura"
    )

    biome_type_ids = fields.Many2many(
        comodel_name="biome.type",
        string="Tipi di Bioma",
        help="Tipi di Bioma"
    )

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""
        MAP_BIOME_IDS = utility_maps[2]
        biomes = list(MAP_BIOME_IDS.keys())
        list_biome_id = [MAP_BIOME_IDS.get(x) for x in biomes if row.get(x) == '1']

        vals = {
            "name": row.get('name'),
            "biome_type_ids": [(6, 0, list_biome_id)]
        }
        return vals
