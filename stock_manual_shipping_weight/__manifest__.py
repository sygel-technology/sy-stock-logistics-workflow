# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Manual Shipping Weight',
    'version': '14.0.1.0.1',
    'author': 'Sygel',
    'category': 'Stock',
    'summary': 'The shipping weight field in pickings can be manually edited.',
    'website': 'https://www.sygel.es',
    'depends': [
        'sale_stock',
        'sale_management',
        'delivery',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'wizard/edit_shipping_weight_wizard_view.xml',
    ],
}
