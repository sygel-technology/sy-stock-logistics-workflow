# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    show_lot_button = fields.Boolean(
        help="If enabled, the icon to display the picking's full lot form view."
    )
    lot_form_as_popup = fields.Boolean(
        string="Open Lot Form as Popup",
        help="If enabled, the lot form view will be displayed in a pop-up.",
    )
