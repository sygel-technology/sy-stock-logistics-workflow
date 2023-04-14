# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Picking(models.Model):
    _inherit = "stock.picking"

    def action_force_availability(self):
        self.ensure_one()
        for move in self.mapped('move_ids_without_package').filtered(
                lambda x: x.product_id.type == "product" 
                and x.product_id.tracking == "none"):
            move.write({'quantity_done': move.product_uom_qty})
        
        if not self.mapped('move_ids_without_package').filtered(
                lambda x: x.product_id.type == "product" 
                and x.product_id.tracking != "none"):
            self.update({'state': 'assigned'})
