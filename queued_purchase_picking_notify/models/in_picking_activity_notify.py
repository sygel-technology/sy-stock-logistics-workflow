# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class InPickingActivityNotify(models.Model):
    _name = "in.picking.activity.notify"
    _description = "Picking Activity Notify"

    _inherit = ["activity.notify.mixin", "in.picking.notify.mixin"]
