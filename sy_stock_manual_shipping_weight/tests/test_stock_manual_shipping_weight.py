# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestStockManualShippingWeight(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.warehouse = cls.env["stock.warehouse"].search([], limit=1)
        cls.picking_type = cls.warehouse.out_type_id
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.picking_type.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "location_dest_id": cls.customer_location.id,
            }
        )

    def test_compute_shipping_weight_with_edited_weight(self):
        self.picking.edited_shipping_weight = 12.5
        self.picking._compute_shipping_weight()
        self.assertEqual(self.picking.shipping_weight, 12.5)

    def test_action_edit_shipping_weight_wizard(self):
        action = self.picking.action_edit_shipping_weight_wizard()
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "edit.shipping.weight.wizard")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
        self.assertEqual(
            action["context"]["default_picking_id"],
            self.picking.id,
        )

    def test_apply_shipping_weight_edition(self):
        wizard = self.env["edit.shipping.weight.wizard"].create(
            {
                "picking_id": self.picking.id,
                "shipping_weight": 15.75,
            }
        )
        wizard.apply_edition()
        self.assertEqual(self.picking.edited_shipping_weight, 15.75)
        self.assertEqual(self.picking.shipping_weight, 15.75)

    def test_apply_shipping_weight_edition_twice(self):
        wizard = self.env["edit.shipping.weight.wizard"].create(
            {
                "picking_id": self.picking.id,
                "shipping_weight": 10.0,
            }
        )
        wizard.apply_edition()
        self.assertEqual(self.picking.shipping_weight, 10.0)
        wizard = self.env["edit.shipping.weight.wizard"].create(
            {
                "picking_id": self.picking.id,
                "shipping_weight": 20.0,
            }
        )
        wizard.apply_edition()
        self.assertEqual(self.picking.edited_shipping_weight, 20.0)
        self.assertEqual(self.picking.shipping_weight, 20.0)

    def test_apply_shipping_weight_only_changes_selected_picking(self):
        second_picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type.id,
                "location_id": self.warehouse.lot_stock_id.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        wizard = self.env["edit.shipping.weight.wizard"].create(
            {
                "picking_id": self.picking.id,
                "shipping_weight": 25.0,
            }
        )
        wizard.apply_edition()
        self.assertEqual(self.picking.edited_shipping_weight, 25.0)
        self.assertFalse(second_picking.edited_shipping_weight)
