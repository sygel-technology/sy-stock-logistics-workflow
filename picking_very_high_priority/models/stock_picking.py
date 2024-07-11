# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    priority = fields.Selection(
        selection_add=[
            ("2", "Very Urgent"),
        ]
    )
