import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)
note_dikts = [
    {'name': 'Diavoli', 'description': 'Aggiungere I signori dei 9 cerchi.'},
    {'name': 'TAG Boss - Signore', 'description': 'Distinguere i due tag.'},
    {'name': 'Nightwalker', 'description': "Ho messo solo shadowfell, ma andrebbe un po' bene ovunque."},
    {'name': 'creature.encounter', 'description': 'aggiungere azione per download_encounters_py.'},
    {'name': 'TAG Any-biome', 'description':
        'Da valutare. Aggiungendo questo tag si aggiungerebbero tutti i biomi, il problema è la rimozione.'},
]


class CreatureCreature(models.Model):
    _name = "todo"
    _description = "TODO"

    name = fields.Char(
        string="Nome",
    )
    description = fields.Text(
        string="Descrizione",
    )

    def popolate_note_dikts(self):
        self.create(note_dikts)
