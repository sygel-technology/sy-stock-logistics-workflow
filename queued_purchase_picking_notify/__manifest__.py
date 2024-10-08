# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued Purchase Picking Notify",
    "summary": "Schedule email/logs/activities notificacions on purchase pickings",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/sygel-technology/sy-stock-logistics-workflow",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["purchase_stock", "queued_purchase_notify"],
    "data": [
        "security/queued_picking_notify_security.xml",
        "security/ir.model.access.csv",
        "views/purchase_order_type_view.xml",
    ],
}
