# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.base_queued_notify.tests.common import TestQueuedNotifyCommon


class TestQueuedPurchasePickingNotify(TestQueuedNotifyCommon):
    def setUp(cls):
        super().setUp()
        notificable_model = cls.env["stock.picking"]
        cls._setUpCommon(
            type_model=cls.env["purchase.order.type"],
            notificable_model=notificable_model,
            relation_field_name=False,
            prefix="picking_",
        )
        cls.product_id = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )
        cls.purchase_id = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner_id.id,
                "order_type": cls.type_record.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_id.id,
                            "product_qty": 1.0,
                        },
                    )
                ],
            }
        )
        cls.purchase_id.button_confirm()
        cls.notificable_record = cls.purchase_id.picking_ids[:1]

    def _create_queues(self):
        return self.notificable_record.button_validate()

    def _get_notify_ids(self):
        return self.type_record._get_picking_notify_ids().values()

    def test_generated_queues(self):
        self.assert_generated_queues()

    def test_notifications(self):
        self.assert_notifications()
