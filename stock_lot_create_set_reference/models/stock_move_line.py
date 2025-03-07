# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_lot_sequence(self):
        self.ensure_one()
        res = super()._get_lot_sequence()
        ml_list = self.env.context.get("skip_vals_set_lot_ref", [])
        ml_list.append(self.id)
        self.env.context = self.with_context(skip_vals_set_lot_ref=ml_list)._context
        return res

    def _prepare_new_lot_vals(self):
        self.ensure_one()
        self.env.context = self.with_context(skip_create_set_lot_ref=True)._context
        res = super()._prepare_new_lot_vals()
        if (
            self.picking_id.picking_type_id.set_name_internal_ref
            and self.id not in self.env.context.get("skip_vals_set_lot_ref", [])
        ):
            sequence_id = self.product_id.lot_sequence_id or self.env.ref(
                "stock.sequence_production_lots"
            )
            res.update(
                {
                    "name": sequence_id._next(),
                    "ref": self.lot_name,
                }
            )
        return res
