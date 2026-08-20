# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Picking Carrier Tracking Ref Search",
    "summary": "Search by carrier_tracking_ref in stock pickings",
    "version": "18.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["delivery", "stock"],
    "data": [
        "views/stock_picking_views.xml",
    ],
}
