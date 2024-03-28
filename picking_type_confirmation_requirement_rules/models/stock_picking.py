# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "confirmation.requirement.mixin"]
    _type_field = {
        "type": "picking_type_id",
    }

    def _action_done(self):
        # Check requirement rules before calling super so shipping is not sent
        # to carrier in case of an error.
        self.check_confirmation_requirements()
        return super()._action_done()
