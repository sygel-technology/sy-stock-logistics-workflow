# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestPickingCarrierTrackingRefSearch(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.env.ref("stock.picking_type_internal").id,
                "location_id": cls.env.ref("stock.stock_location_stock").id,
                "location_dest_id": cls.env.ref("stock.stock_location_stock").id,
                "carrier_tracking_ref": "TEST-TRACKING-123",
            }
        )

    def test_search_by_carrier_tracking_ref(self):
        picking = self.env["stock.picking"].search(
            [("carrier_tracking_ref", "ilike", "TRACKING-123")]
        )
        self.assertIn(self.picking, picking)

    def test_carrier_tracking_ref_index(self):
        field = self.env["stock.picking"]._fields["carrier_tracking_ref"]
        self.assertEqual(field.index, "trigram")
