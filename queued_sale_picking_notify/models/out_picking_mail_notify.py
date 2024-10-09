# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class OutPickingMailNotify(models.Model):
    _name = "out.picking.mail.notify"
    _description = "Picking Mail Notify"

    _inherit = ["mail.notify.mixin", "out.picking.notify.mixin"]
