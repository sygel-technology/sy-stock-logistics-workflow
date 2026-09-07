# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock Manual Shipping Weight",
    "summary": "The shipping weight field in pickings can be manually edited.",
    "version": "17.0.1.0.0",
    "author": "Sygel",
    "license": "AGPL-3",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "depends": [
        "sale_stock",
        "sale_management",
        "stock_delivery",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_view.xml",
        "wizard/edit_shipping_weight_wizard_view.xml",
    ],
}
