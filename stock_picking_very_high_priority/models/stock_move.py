# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    priority = fields.Selection(
        selection_add=[
            ("2", "Very Urgent"),
        ]
    )

    @api.depends("picking_type_id", "date", "priority")
    def _compute_reservation_date(self):
        res = None
        for move in self:
            if (
                move.priority == "2"
                and move.picking_type_id.reservation_method == "by_date"
                and move.state
                in ["draft", "confirmed", "waiting", "partially_available"]
            ):
                days = move.picking_type_id.reservation_days_before_priority
                move.reservation_date = fields.Date.to_date(move.date) - timedelta(
                    days=days
                )
            else:
                res = super(StockMove, move)._compute_reservation_date()
        return res
