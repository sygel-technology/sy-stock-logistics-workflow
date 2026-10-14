# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    assign_responsible_on_validate = fields.Boolean(
        string="Assign Responsible on Validation",
        help=(
            "If enabled, the user validating the picking will be set as responsible "
            "if none is defined."
        ),
    )
