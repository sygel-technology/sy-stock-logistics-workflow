# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PickingLogNoteNotify(models.Model):
    _name = "picking.log.note.notify"
    _description = "Picking Mail Notify"

    reference_field = fields.Selection(
        [
            ("scheduled_date", "Scheduled Date"),
            ("purchase_shipping_date", "Purchase Shipping Date"),
        ],
        name="Reference Field",
        required=True,
    )
    empty_field = fields.Selection(
        [
            ("carrier_id", "Carrier"),
            ("purchase_shipping_date", "Purchase Shipping Date"),
        ],
        name="Empty Field",
        required=True,
    )
    notify_when = fields.Selection(
        [("before", "Before"), ("after", "After")],
        name="Reference Field",
        required=True,
    )
    notify_time = fields.Float(name="Notify Time (Hours)")
    note_text = fields.Char(name="Note Text")
    purchase_order_type_id = fields.Many2one(
        name="Purchase Order Type", comodel_name="purchase.order.type"
    )

    @api.multi
    @api.constrains("reference_field", "empty_field")
    def _check_reference_field_empty_field(self):
        for sel in self:
            if sel.reference_field == sel.empty_field:
                raise ValidationError(
                    _("Reference Field and Empty Field cannot be equal.")
                )
