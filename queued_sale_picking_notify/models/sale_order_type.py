# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    picking_mail_notify_ids = fields.One2many(
        name="Picking Mail Notifications",
        comodel_name="out.picking.mail.notify",
        inverse_name="sale_order_type_id",
    )
    picking_log_note_notify_ids = fields.One2many(
        name="Picking Log Note Notifications",
        comodel_name="out.picking.log.note.notify",
        inverse_name="sale_order_type_id",
    )
    picking_activity_notify_ids = fields.One2many(
        name="Picking Activity Notifications",
        comodel_name="out.picking.activity.notify",
        inverse_name="sale_order_type_id",
    )

    def _get_picking_notify_ids(self):
        return {
            "picking_mail_notify_ids": self.picking_mail_notify_ids,
            "picking_log_note_notify_ids": self.picking_log_note_notify_ids,
            "picking_activity_notify_ids": self.picking_activity_notify_ids,
        }
