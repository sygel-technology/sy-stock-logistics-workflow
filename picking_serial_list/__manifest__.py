# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Picking Serial List",
    "version": "14.0.3.0.0",
    "category": "Stock",
    "author": "Sygel, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    'data': [
        "views/stock_picking_views.xml",
    ],
    "application": False,
    "installable": True,
}
