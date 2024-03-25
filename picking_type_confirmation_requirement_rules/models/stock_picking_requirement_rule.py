# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockPickingRequiredRule(models.Model):
    _name = "stock.picking.requirement.rule"
    _inherit = ["confirmation.requirement.rule.mixin"]
    _description = "Stock Picking Required Rule"
