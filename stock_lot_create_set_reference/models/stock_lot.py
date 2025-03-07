# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.lot"

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("skip_create_set_lot_ref"):
            return super().create(vals_list)
        for vals in vals_list:
            product_id = self.env["product.product"].browse(
                vals.get("product_id") or self.env.context.get("default_product_id")
            )
            picking_id = self.env["stock.picking"].browse(
                self.env.context.get("active_picking_id")
            )
            sequence_id = product_id.lot_sequence_id or self.env.ref(
                "stock.sequence_production_lots"
            )
            if picking_id.picking_type_id.set_name_internal_ref:
                vals.update(
                    {
                        "name": sequence_id._next(),
                        "ref": vals.get("name"),
                    }
                )
        return super().create(vals_list)
