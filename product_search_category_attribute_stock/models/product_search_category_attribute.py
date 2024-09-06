# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSearchCatAttr(models.AbstractModel):
    _inherit = "product.search.cat.attr"

    search_on_hand = fields.Boolean(
        help="Only show stockable products with 'On hand' quantity greater "
        "than 0. Service and consumable products are always shown."
    )
    search_forecasted = fields.Boolean(
        help="Only show stockable products with an available quantity greater "
        "than 0 on the date set in 'Stock Date'. Service and consumable "
        "products are always shown."
    )
    stock_date = fields.Date(
        default=fields.Date.context_today,
        help="If 'Search on hand' or 'Search forecasted' options are active, "
        "consider stock on this date.",
    )

    def _search_products(self):
        products = super()._search_products()
        if self.search_on_hand or self.search_forecasted:
            filtered_products = self.env["product.product"]
            date = self.stock_date or fields.Date.context_today
            if self.search_on_hand:
                filtered_products = products.filtered(
                    lambda a: a.type in ["consu", "service"]
                    or a.with_context(to_date=date).qty_available > 0.0
                )
            if self.search_forecasted:
                filtered_products += products.filtered(
                    lambda a: (
                        a.type in ["consu", "service"]
                        or a.with_context(to_date=date).virtual_available > 0.0
                    )
                    and a.id not in filtered_products.ids
                )
            products = filtered_products
        return products
