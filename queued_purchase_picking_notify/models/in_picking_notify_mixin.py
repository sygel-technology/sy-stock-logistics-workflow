# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class InPickingNotifyMixin(models.AbstractModel):
    _name = "in.picking.notify.mixin"
    _description = "Mixin for queued picking notification events"

    _inherit = "notify.mixin"

    notified_model_name = "stock.picking"

    trigger_state = fields.Selection(
        selection_add=[
            ("in_picking", "Done Pickings"),
        ],
        default="in_picking",
        required=True,
        ondelete={
            "in_picking": "cascade",
        },
    )

    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type", comodel_name="purchase.order.type"
    )

    def is_to_notify(self, record):
        # Returns if a record is in a status to be notified
        if self.trigger_state == "in_picking":
            res = record.state == "done" and record.picking_type_code == "incoming"
            return res
        else:
            return False
