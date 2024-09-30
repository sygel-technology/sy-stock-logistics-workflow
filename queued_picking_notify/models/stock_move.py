from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_supplier_code = fields.Char(
        compute="_compute_product_supplier_code",
        string="Product Supplier Code",
        store=True,
        size=64,
    )
    product_supplier_description = fields.Char(
        compute="_compute_product_supplier_code",
        string="Product Supplier Description",
        store=True,
        size=64,
    )

    @api.multi
    @api.depends(
        "picking_id.partner_id", "product_id", "product_id.seller_ids.product_code"
    )
    def _compute_product_supplier_code(self):
        for move in self.filtered(
            lambda m: m.picking_id
            and m.picking_id.partner_id
            and m.product_tmpl_id.seller_ids
        ):
            suppliers = move.product_tmpl_id.seller_ids.filtered(
                lambda m: m.name.id == move.picking_id.partner_id.id
                or m.name.id == move.picking_id.partner_id.parent_id.id
            )
            if suppliers:
                move.product_supplier_code = suppliers[0].product_code
                move.product_supplier_description = suppliers[0].product_name
            else:
                move.product_supplier_code = ""
                move.product_supplier_description = ""
