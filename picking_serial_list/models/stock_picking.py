# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_reserve_list_serial = fields.Boolean(
        compute="_compute_show_reserve_list_serial"
    )

    @api.depends(
        "move_ids_without_package",
        "move_ids_without_package.move_line_ids",
        "move_ids_without_package.move_line_nosuggest_ids"
    )
    def _compute_show_reserve_list_serial(self):
        for sel in self:
            show = False
            for line in self.move_ids_without_package:
                if line.picking_type_id.show_reserved and line.move_line_ids.filtered(
                        lambda a: a.forced_update_serial_qty and a.product_uom_qty < a.qty_done
                ):
                    show = True
                elif line.move_line_nosuggest_ids.filtered(
                        lambda a: a.forced_update_serial_qty and a.product_uom_qty < a.qty_done
                ):
                    show = True
            sel.show_reserve_list_serial = show

    def action_reserve_list_serial(self):
        lines = self.env['stock.move.line']
        for line in self.move_ids_without_package:
            if line.picking_type_id.show_reserved and line.move_line_ids.filtered(
                lambda a: a.forced_update_serial_qty and a.product_uom_qty < a.qty_done
            ):
                lines += line.move_line_ids.filtered(
                    lambda a: a.forced_update_serial_qty
                )
            elif line.move_line_nosuggest_ids.filtered(
                lambda a: a.forced_update_serial_qty and a.product_uom_qty < a.qty_done
            ):
                lines += line.move_line_nosuggest_ids.filtered(
                    lambda a: a.forced_update_serial_qty
                )
        if lines:
            stock_move_ids = lines.mapped('move_id')
            stock_move_ids._do_unreserve()
            for line in lines:
                quantity = self.env['stock.quant']._get_available_quantity(
                    line.product_id,
                    line.location_id,
                    line.lot_id
                )
                if quantity > 0.0:
                    line._get_quant(line.lot_id)
                    line.write({
                        'product_uom_qty': 1.0
                    })
            stock_move_ids._recompute_state()
