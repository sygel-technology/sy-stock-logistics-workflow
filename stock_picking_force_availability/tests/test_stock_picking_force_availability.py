# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStockPickingForceAvailability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "is_storable": True,
                "tracking": "none",
            }
        )
        cls.picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Test Delivery",
                "sequence_code": "TEST",
                "allow_force_availability": True,
            }
        )

    def test_stock_picking_force_availability(self):
        pick_out = self.env["stock.picking"].create(
            {
                "partner_id": self.partner.id,
                "picking_type_id": self.picking_type.id,
                "state": "waiting",
                "move_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "name": "test_out_line",
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "quantity": 0.0,
                        },
                    )
                ],
            }
        )
        pick_out.action_force_availability()
        self.assertEqual(pick_out.move_ids_without_package.quantity, 1)
        self.assertEqual(pick_out.state, "assigned")
        pick_out.button_validate()
