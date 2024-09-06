# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Search Category Attribute - Stock",
    "summary": "Search products by category and attributes considering availability",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock", "product_search_category_attribute"],
    "data": ["views/product_search_category_attribute_views.xml"],
}
