# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            if (
                picking.picking_type_id.assign_responsible_on_validate
                and not picking.user_id
            ):
                picking.user_id = self.env.user
        return super().button_validate()
