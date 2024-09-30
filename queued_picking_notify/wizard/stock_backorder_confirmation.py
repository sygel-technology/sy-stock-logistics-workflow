# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockBackorderConfirmation(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    def process(self):
        super(StockBackorderConfirmation, self)._process()
        for pick in self.pick_ids:
            for picking in pick.backorder_ids:
                if not picking.purchase_shipping_date:
                    picking.picking_notify_shipping_date()
                if not picking.carrier_id:
                    picking.picking_notify_carrier()
