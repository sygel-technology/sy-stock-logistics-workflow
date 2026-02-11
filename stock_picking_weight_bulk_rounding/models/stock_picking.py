# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import float_round


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends(
        "move_line_ids",
        "move_line_ids.result_package_id",
        "move_line_ids.product_uom_id",
        "move_line_ids.quantity",
    )
    def _compute_bulk_weight(self):
        # This method is overridden to normalize the value sent in shipping_weight.
        # In some cases the computed weight contained excessive float decimals
        # (e.g. 6.8000000000001) and was sent to the carrier, causing validation errors.
        super()._compute_bulk_weight()
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for picking in self:
            picking.weight_bulk = float_round(
                picking.weight_bulk, precision_digits=precision
            )
        return
