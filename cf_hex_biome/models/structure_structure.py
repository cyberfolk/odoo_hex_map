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

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        string="Biomi",
        help="Biomi dove si può trovare la struttura"
    )

    def cf_to_odoo_dict(self, row, utility_maps):
        """Traduce una riga di un file csv in un dizionario 'odoo_dict'."""
        MAP_BIOME_IDS = utility_maps[2]
        biome_names = row.get('Biomi')
        biome_ids = [MAP_BIOME_IDS.get(x) for x in biome_names]
        vals = {
            "name": row.get('Nome'),
            "biome_ids": [(6, 0, biome_ids)]
        }
        return vals
