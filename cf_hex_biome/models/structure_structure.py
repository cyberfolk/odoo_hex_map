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
        biome_type_names = row.get('Tipi di Bioma')
        biome_type_ids = [MAP_BIOME_IDS.get(x) for x in biome_type_names]
        vals = {
            "name": row.get('Nome'),
            "biome_type_ids": [(6, 0, biome_type_ids)]
        }
        return vals
