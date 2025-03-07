# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    in_mail_queue_ids = fields.Many2many(
        string="Purchase Queues",
        comodel_name="queue.job",
        compute="_compute_in_mail_queues",
    )

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            notity_set = rec.purchase_id.order_type._get_picking_notify_ids()
            for notify_ids in notity_set.values():
                for notify_id in notify_ids:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res

    def button_validate(self):
        res = super().button_validate()
        for rec in self:
            notity_set = rec.purchase_id.order_type._get_picking_notify_ids()
            for notify_ids in notity_set.values():
                for notify_id in notify_ids:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res

    def _compute_in_mail_queues(self):
        for obj in self:
            obj.in_mail_queue_ids = (
                self.env["queue.job"]
                .search(
                    [
                        [
                            "func_string",
                            "=like",
                            f"in.picking.mail.notify(%,)._notify_thread(stock.picking({obj.id},))",
                        ]
                    ]
                )
                .ids
            )
