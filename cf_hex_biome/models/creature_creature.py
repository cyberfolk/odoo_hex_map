import csv
import logging
from pathlib import Path

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _name = "creature.creature"
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

    def popolate_creature(self):
        """Crea le creature partendo da un file csv
        """
        # Recupero il path del file CSV dove sono presenti le creature
        creatures_path = (Path(__file__).resolve().parents[1] / 'data' / 'creatures.csv').as_posix()

        # Creo delle mappe di conversione {nome: id} per i tipi e i tag delle creature
        map_types_ids = {x.name: x.id for x in self.env['creature.type'].search([])}
        map_tags_ids = {x.name: x.id for x in self.env['creature.tag'].search([])}
        try:
            with open(creatures_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    tag_field_list =['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7']
                    tag_list = [row.get(tag) for tag in tag_field_list]
                    tag_ids_list = [map_tags_ids[tag] for tag in tag_list if tag]
                    vals = {
                        'skip': bool(row.get('skip')),
                        'cool': bool(row.get('cool')),
                        'type_id': map_types_ids[row.get('Tipo')],
                        'tag_ids': [(6, 0, tag_ids_list)],
                        'name': row.get('Creature'),
                        'link_5et': row.get('Link'),
                        'cr': float(row.get('CR').replace(',', '.')) or 0,
                    }
                    self.create(vals)
                    _logger.info(f"{i} Creatura {row.get('Creature')} creata!")
        except Exception as e:
            _logger.error(f"Errore durante l'importazione: {e}")

        _logger.info("Importazione delle creature terminata!")
