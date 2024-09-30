# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Queued Picking Notify",
    "summary": "Send email/logs/activities notificacions from pickings",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "queue_job",
        "purchase_order_type",
        "purchase_picking_notify_interface",
        "stock",
        "ea_base",
        "purchase_stock",
    ],
    "data": [
        'views/view_purchase_order_type_form.xml',
        'views/stock_picking_views.xml',
        'data/mail_data.xml',
        'security/queued_picking_notify_security.xml',
        'security/ir.model.access.csv',
    ],
}
