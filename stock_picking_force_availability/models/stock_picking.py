# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    allow_force_availability = fields.Boolean(
        related="picking_type_id.allow_force_availability",
        string="Allow to Force Availability",
    )

    def action_force_availability(self):
        self.ensure_one()
        for move in self.mapped("move_ids_without_package").filtered(
            lambda x: x.product_id.type == "product" and x.product_id.tracking == "none"
        ):
            move.write({"quantity_done": move.product_uom_qty})

        if not self.mapped("move_ids_without_package").filtered(
            lambda x: x.product_id.type == "product" and x.product_id.tracking != "none"
        ):
            self.update({"state": "assigned"})


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    allow_force_availability = fields.Boolean(
        default=False,
        string="Allow to Force Availability",
    )
