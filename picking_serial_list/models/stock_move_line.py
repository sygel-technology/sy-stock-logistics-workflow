# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    forced_update_serial_qty = fields.Boolean()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('forced_update_serial_qty'):
                vals['product_uom_qty'] = 1.0
        return super().create(vals_list)
        