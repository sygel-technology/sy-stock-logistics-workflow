# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.tools.float_utils import float_compare


class TestStockPickingWeightBulkRounding(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product Weight",
                "type": "product",
                "weight": 0.2,
            }
        )

        cls.location_src = cls.env.ref("stock.stock_location_stock")
        cls.location_dest = cls.env.ref("stock.stock_location_customers")

        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.env.ref("stock.picking_type_out").id,
                "location_id": cls.location_src.id,
                "location_dest_id": cls.location_dest.id,
            }
        )

        cls.move = cls.env["stock.move"].create(
            {
                "name": "Test Move",
                "product_id": cls.product.id,
                "product_uom_qty": 3,
                "product_uom": cls.product.uom_id.id,
                "picking_id": cls.picking.id,
                "location_id": cls.location_src.id,
                "location_dest_id": cls.location_dest.id,
            }
        )

        cls.move._action_confirm()
        cls.move._action_assign()

        cls.env["stock.move.line"].create(
            {
                "move_id": cls.move.id,
                "picking_id": cls.picking.id,
                "product_id": cls.product.id,
                "product_uom_id": cls.product.uom_id.id,
                "quantity": 3,
                "location_id": cls.location_src.id,
                "location_dest_id": cls.location_dest.id,
            }
        )

    def test_weight_bulk_is_rounded(self):
        self.picking._compute_bulk_weight()

        expected = 0.6

        self.assertEqual(
            float_compare(
                self.picking.weight_bulk,
                expected,
                precision_digits=6,
            ),
            0,
            "weight_bulk should be correctly rounded to 0.6",
        )
