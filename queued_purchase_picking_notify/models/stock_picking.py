# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Picking(models.Model):
    _inherit = "stock.picking"

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            notity_set = rec.purchase_id.order_type._get_picking_notify_ids()
            for notify_ids in notity_set.values():
                for notify_id in notify_ids:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res

    def write(self, values):
        res = super().write(values)
        for rec in self:
            notity_set = rec.purchase_id.order_type._get_picking_notify_ids()
            for notify_ids in notity_set.values():
                for notify_id in notify_ids:
                    if notify_id.is_to_notify(rec):
                        notify_id.notify(rec)
        return res
