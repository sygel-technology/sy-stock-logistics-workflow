# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _create_picking(self):
        res = super()._create_picking()
        notity_set = self.order_type._get_picking_notify_ids()
        for notify_ids in notity_set.values():
            for notify_id in notify_ids:
                for picking in self.picking_ids:
                    if notify_id.is_to_notify(picking):
                        notify_id.notify(picking)
        return res
