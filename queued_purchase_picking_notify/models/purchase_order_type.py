# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    picking_mail_notify_ids = fields.One2many(
        name="Picking Mail Notifications",
        comodel_name="in.picking.mail.notify",
        inverse_name="purchase_order_type_id",
    )
    picking_log_note_notify_ids = fields.One2many(
        name="Picking Log Note Notifications",
        comodel_name="in.picking.log.note.notify",
        inverse_name="purchase_order_type_id",
    )
    picking_activity_notify_ids = fields.One2many(
        name="Picking Activity Notifications",
        comodel_name="in.picking.activity.notify",
        inverse_name="purchase_order_type_id",
    )

    def _get_picking_notify_ids(self):
        return {
            "picking_mail_notify_ids": self.picking_mail_notify_ids,
            "picking_log_note_notify_ids": self.picking_log_note_notify_ids,
            "picking_activity_notify_ids": self.picking_activity_notify_ids,
        }
