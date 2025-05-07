# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    show_lot_button = fields.Boolean(
        compute="_compute_show_lot_button",
    )

    def action_open_lot_form(self):
        self.ensure_one()
        result = False
        if self.lot_id:
            result = {
                "type": "ir.actions.act_window",
                "name": "Lot",
                "res_model": "stock.lot",
                "view_mode": "form",
                "res_id": self.lot_id.id,
                "target": "new"
                if self.picking_id.picking_type_id.lot_form_as_popup
                else "current",
            }
        else:
            raise UserError(_("You must select a lot before opening the form."))
        return result

    @api.depends("picking_id.picking_type_id.show_lot_button")
    def _compute_show_lot_button(self):
        for line in self:
            line.show_lot_button = line.picking_id.picking_type_id.show_lot_button
