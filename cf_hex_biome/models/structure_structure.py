from odoo import fields, models
from ..data.map_structure_biome import MAP_STRUCTURE_BIOME


class StructureStructure(models.Model):
    _name = "structure.structure"
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

    def popolate_structure_biome(self):
        """Crea le strutture e le collega ai biomi basandosi sul dizionario MAP_STRUCTURE_BIOME.
        È fragile perchè usa come indici per il collegamento:
         - il name della structure.structure
         - il name del biome.tipe
        """
        dict_biome_type_id = {b.name: b.id for b in self.env["biome.type"].search([])}
        for structure, list_biome_name in MAP_STRUCTURE_BIOME.items():
            list_biome_id = [dict_biome_type_id[b] for b in list_biome_name]
            self.create({
                "name": structure,
                "biome_type_ids": [(6, 0, list_biome_id)]
            })
