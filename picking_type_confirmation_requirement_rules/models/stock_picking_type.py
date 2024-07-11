# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PickingType(models.Model):
    _name = "stock.picking.type"
    _inherit = ["stock.picking.type", "requirement.rule.type.mixin"]

    requirement_rule_ids = fields.Many2many(
        comodel_name="stock.picking.requirement.rule",
        relation="picking_confirmation_requirement_rule_type_rel",
    )
