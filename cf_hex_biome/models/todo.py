old_note = [
    ("Cloackwork - Trovare un Bioma per i costrutti",
     "Al momento l'ho l'asciato in bianco perchè starebbero ovunque, ma c'è da trovare una soluzione più elegante."),
    ("TAG NPC", "Ho rimosso ogni bioma da loro."),
    ("TAG Any-biome",
     "Valutare se farlo. Aggiungendo quel tag si andrebbero a mettere tutti i biomi, il problema è la rimozione."),
    ("Tag  auto-set-biome", "Valutare la fattibilità."),
    ("Diavoli", "Aggiungere signori inferno."),
    ("TAG Boss - Signore", "Distinguere i due tag."),
    ("Nightwalker", "Ho messo solo shadowfell, ma andrebbe un po' bene ovunque."),
    ("creature.encounter", "aggiungere azione per download_encounters_py."),
]
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _name = "todo"
    _description = "TODO"

    name = fields.Char(
        string="Nome",
    )
    description = fields.Text(
        string="Descrizione",
    )
