from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('move_line_ids.result_package_id',
                 'move_line_ids.result_package_id.shipping_weight',
                 'weight_bulk', 'edited_shipping_weight')
    def _compute_shipping_weight(self):
        for picking in self:
            if picking.edited_shipping_weight > 0:
                picking.shipping_weight = picking.edited_shipping_weight
            else:
                return super(StockPicking, picking)._compute_shipping_weight()

    edited_shipping_weight = fields.Float(string='Edited Shipping Weight',
                                          help='Total weight of the package edited with wizard.')

    def action_edit_shipping_weight_wizard(self):
        return {
            'name': _('Edit weight'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'edit.shipping.weight.wizard',
            'view_id': self.env.ref('stock_manual_shipping_weight.edit_shipping_weight_wizard_view_form').id,
            'target': 'new',
            'context': {'default_picking_id': self.id},
        }
