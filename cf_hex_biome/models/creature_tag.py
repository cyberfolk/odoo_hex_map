from odoo import fields, models, api


class CreatureTag(models.Model):
    _name = "creature.tag"
    _description = "Tag per creature"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Tag per creature"
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        string="Creature",
        help="Creature con questo tag"
    )

    is_faction = fields.Boolean(
        string="Fazione",
        help="È una fazione?",
        default=False
    )

    kanban_is_faction_label = fields.Char(
        string="Kanban Etichetta Fazione",
        compute='_compute_kanban_is_faction_label',
        store=True,
        help="Campo utility per impostare l'etichetta del raggruppamento per fazione nella vista kanban.",
    )

    @api.depends('is_faction')
    def _compute_kanban_is_faction_label(self):
        for record in self:
            record.kanban_is_faction_label = 'Fazione' if record.is_faction else 'NON Fazione'
