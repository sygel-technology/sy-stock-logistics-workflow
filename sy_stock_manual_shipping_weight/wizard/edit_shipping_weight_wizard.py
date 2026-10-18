# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EditShippingWeightWizard(models.TransientModel):
    _name = "edit.shipping.weight.wizard"
    _description = "Edit Shipping Weight At Picking"

    picking_id = fields.Many2one(
        "stock.picking",
        string="Picking",
    )

    shipping_weight = fields.Float(
        string="New Shipping Weight", help="Total weight of the package."
    )

    def apply_edition(self):
        picking = self.env["stock.picking"].search(
            [("id", "=", self.picking_id.id)], limit=1
        )
        picking.write({"edited_shipping_weight": self.shipping_weight})
        picking._compute_shipping_weight()
