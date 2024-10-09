# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class OutPickingNotifyMixin(models.AbstractModel):
    _name = "out.picking.notify.mixin"
    _description = "Mixin for queued picking notification events"

    _inherit = "notify.mixin"

    notified_model_name = "stock.picking"

    trigger_state = fields.Selection(
        selection_add=[
            ("out_picking", "Done Pickings"),
        ],
        default="out_picking",
        required=True,
        ondelete={
            "out_picking": "cascade",
        },
    )

    sale_order_type_id = fields.Many2one(
        name="Sale Order Type", comodel_name="sale.order.type"
    )

    def is_to_notify(self, record):
        if self.trigger_state == "out_picking":
            return record.state == "done" and record.picking_type_code == "outgoing"
        else:
            return False
