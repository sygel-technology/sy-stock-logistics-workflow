# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models, _

from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('move_line_ids', 'move_line_nosuggest_ids')
    def onchange_move_line_ids(self):
        ret = super().onchange_move_line_ids()
        if self.picking_type_id.use_serial_list:
            serial_error = []
            breaking_char = '\n'
            if self.picking_type_id.show_reserved:
                move_lines = self.move_line_ids
            else:
                move_lines = self.move_line_nosuggest_ids
            for move_line in move_lines.filtered(
                lambda a: a.product_id.tracking == 'serial'
            ):
                if move_line.lot_name and not move_line.forced_update_serial_qty:
                    # ONLY ONE SERIAL NUMBER
                    if breaking_char not in (move_line.lot_name or ''):
                        lot_id = self.env['stock.production.lot'].search([
                            ('company_id', '=', self.company_id.id),
                            ('product_id', '=', self.product_id.id),
                            ('name', '=', move_line.lot_name),
                        ], limit=1)
                        if lot_id and self.product_id.with_context(lot_id=lot_id.id, location_id=False).qty_available == 1.0:
                            quant = self.env['stock.quant']._get_available_quantity(
                                self.product_id,
                                move_line.location_id,
                                lot_id
                            )
                            if quant > 0.0:
                                move_line.lot_id = lot_id.id
                                move_line.forced_update_serial_qty = True
                                quant_id = move_line._find_quants(
                                    self.product_id,
                                    move_line.location_id,
                                    lot_id
                                )
                                if quant_id:
                                    move_line.location_id = quant_id.location_id.id
                            else:
                                serial_error.append(lot_id.name)
                                move_line.forced_update_serial_qty = False
                        if serial_error:
                            raise ValidationError(_('No available stock for serial(s) %s', serial_error))
                    
                    # MULTIPLE SERIAL NUMBERS
                    elif breaking_char in (move_line.lot_name or ''):
                        # # FIRST SERIAL NUMBER
                        location = move_line.location_id
                        split_lines = move_line.lot_name.split(breaking_char)
                        split_lines = list(filter(None, split_lines))
                        move_line.lot_name = split_lines[0]
                        lot_id = self.env['stock.production.lot'].search([
                            ('company_id', '=', self.company_id.id),
                            ('product_id', '=', self.product_id.id),
                            ('name', '=', split_lines[0]),
                        ], limit=1)
                        if lot_id and self.product_id.with_context(lot_id=lot_id.id, location_id=False).qty_available == 1.0:
                            quant = self.env['stock.quant']._get_available_quantity(
                                self.product_id,
                                location,
                                lot_id
                            )
                            if quant > 0.0:
                                move_line.lot_id = lot_id.id
                                move_line.forced_update_serial_qty = True
                                quant_id = move_line._find_quants(
                                    self.product_id,
                                    location,
                                    lot_id
                                )
                                if quant_id:
                                    move_line.location_id = quant_id.location_id.id
                            else:
                                serial_error.append(lot_id.name)
                                move_line.forced_update_serial_qty = False

                        # REST OF SERIAL NUMBERS
                        move_lines_commands = self._generate_serial_move_line_commands(
                            split_lines[1:],
                            origin_move_line=move_line,
                        )
                        for line in move_lines_commands:
                            line = line[2]
                            lot_id = self.env['stock.production.lot'].search([
                                ('company_id', '=', self.company_id.id),
                                ('product_id', '=', self.product_id.id),
                                ('name', '=', line.get('lot_name')),
                            ], limit=1)
                            if lot_id and self.product_id.with_context(lot_id=lot_id.id, location_id=False).qty_available == 1.0:
                                line['lot_id'] = lot_id.id
                                quant = self.env['stock.quant']._get_available_quantity(
                                    self.product_id,
                                    location,
                                    lot_id
                                )
                                if quant > 0.0:
                                    line.update({
                                        'forced_update_serial_qty': True
                                    })
                                    quant_id = move_line._find_quants(
                                        self.product_id,
                                        location,
                                        lot_id
                                    )
                                    if quant_id:
                                        line.update({
                                            'location_id': quant_id.location_id.id
                                        })
                                else:
                                    serial_error.append(lot_id.name)

                        if not serial_error:
                            if self.picking_type_id.show_reserved:
                                self.update({'move_line_ids': move_lines_commands})
                            else:
                                self.update({'move_line_nosuggest_ids': move_lines_commands})
                        else:
                            raise ValidationError(_('No available stock for serial(s) %s', serial_error))

        return ret

    def action_show_details(self):
        ret_vals = super().action_show_details()
        if self.product_id and self.product_id.tracking == 'serial':
            ret_vals['context']['show_serial_list'] = self.picking_type_id.use_serial_list
        return ret_vals

    def write(self, vals):
        ret = super().write(vals)
        self.filtered(
            lambda a: any(
                line.forced_update_serial_qty for line in a.move_line_ids
            ) or any(
                line.forced_update_serial_qty for line in a.move_line_nosuggest_ids
            )
        )._recompute_state()

        return ret
