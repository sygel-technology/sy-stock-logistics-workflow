# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    use_serial_list = fields.Boolean(
        string="Use Serial List",
    )

    @api.constrains('use_serial_list', 'use_create_lots', 'use_existing_lots', 'show_operations')
    def _check_use_serial_list(self):
        for sel in self.filtered(
            lambda a: a.use_serial_list
        ):
            error_msg = ''
            if sel.use_create_lots:
                error_msg += _(
                    "\nIf 'User Serial List' is checked, 'Create New Lots/Serial Numbers' must be unchecked."
                )
            if not sel.use_existing_lots:
                error_msg += _(
                    "\nIf 'User Serial List' is checked, 'Use Existing Lots/Serial Numbers' must be checked."
                )
            if sel.show_operations:
                error_msg += _(
                    "\nIf 'User Serial List' is checked, 'Show Detailed Operations' must be unchecked."
                )
            if error_msg:
                raise UserError(error_msg)
