# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def _create_picking(self):
        super(PurchaseOrder, self)._create_picking()
        for picking in self.picking_ids:
            if not picking.carrier_id:
                picking.picking_notify_carrier()
            if not picking.purchase_shipping_date:
                picking.picking_notify_shipping_date()
        return True
