# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Picking(models.Model):
    _inherit = "stock.picking"

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
