# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_user_id = fields.Many2one(
        comodel_name="res.users", string="Responsible", related="picking_id.user_id"
    )
