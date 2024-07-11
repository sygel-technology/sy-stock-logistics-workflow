# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Picking Type Confirmation Requirement Rules",
    "version": "15.0.1.0.0",
    "summary": "Required domain conditions when validating a Picking.",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Stock",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "base_confirmation_requirement_rules",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_picking_requirement_rule_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}
