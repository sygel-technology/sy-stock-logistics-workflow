# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Picking Responsible Autoassign",
    "summary": "Assign the validating user as responsible on picking validation",
    "version": "17.0.1.0.0",
    "category": "Inventory",
    "author": "Sygel",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": ["stock"],
    "data": [
        "views/stock_picking_type_views.xml",
    ],
}
