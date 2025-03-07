# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    out_mail_queue_ids = fields.Many2many(
        string="Sale Queues",
        comodel_name="queue.job",
        compute="_compute_out_mail_queues",
    )

    def button_validate(self):
        res = super().button_validate()
        if self.sale_id:
            notity_set = self.sale_id.type_id._get_picking_notify_ids()
            for notify_ids in notity_set.values():
                for notify_id in notify_ids:
                    for rec in self:
                        if notify_id.is_to_notify(rec):
                            notify_id.notify(rec)
        return res

    def _compute_out_mail_queues(self):
        for obj in self:
            obj.out_mail_queue_ids = (
                self.env["queue.job"]
                .search(
                    [
                        [
                            "func_string",
                            "=like",
                            f"out.picking.mail.notify(%,)._notify_thread(stock.picking({obj.id},))",
                        ]
                    ]
                )
                .ids
            )
