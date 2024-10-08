# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class OutPickingNoteNotify(models.Model):
    _name = "out.picking.log.note.notify"
    _description = "Picking Note Notify"

    _inherit = ["note.notify.mixin", "out.picking.notify.mixin"]
