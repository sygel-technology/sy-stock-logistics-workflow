# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class OutPickingActivityNotify(models.Model):
    _name = "out.picking.activity.notify"
    _description = "Picking Activity Notify"

    _inherit = ["activity.notify.mixin", "out.picking.notify.mixin"]
