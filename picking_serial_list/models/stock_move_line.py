# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    forced_update_serial_qty = fields.Boolean()

    def _find_quants(self, product, location, lot):
        return self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', 'child_of', location.id),
            ('lot_id', '=', lot.id)
        ], limit=1)

    def _get_quant(self, lot_id):
        quant = False
        quants = self.env['stock.quant']._update_reserved_quantity(
            self.product_id, self.location_id, 1, lot_id
        )
        if quants:
            quant = quants[0][0]
        return quant
        