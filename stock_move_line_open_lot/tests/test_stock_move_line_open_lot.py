# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestStockMoveLineOpenLot(TransactionCase):
    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "tracking": "lot",
            }
        )

        self.lot = self.env["stock.lot"].create(
            {
                "name": "LOT001",
                "product_id": self.product.id,
            }
        )

        self.stock_location = self.env["stock.location"].search(
            [("name", "=", "Stock")], limit=1
        )

        self.stock_location_dest = self.env["stock.location"].search(
            [("name", "=", "Customers")], limit=1
        )

        self.picking_type_default = self.env["stock.picking.type"].create(
            {
                "name": "Default Picking Type",
                "sequence_code": "PT1",
                "show_lot_button": True,
            }
        )
        self.picking_type_popup = self.env["stock.picking.type"].create(
            {
                "name": "Popup Picking Type",
                "sequence_code": "PT2",
                "lot_form_as_popup": True,
            }
        )

        self.picking_default = self.env["stock.picking"].create(
            {
                "name": "Picking Default",
                "picking_type_id": self.picking_type_default.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location_dest.id,
            }
        )

        self.picking_popup = self.env["stock.picking"].create(
            {
                "name": "Picking Popup",
                "picking_type_id": self.picking_type_popup.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location_dest.id,
            }
        )

        self.move = self.env["stock.move"].create(
            {
                "name": "Test Move",
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "product_uom": self.product.uom_id.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location_dest.id,
                "picking_id": self.picking_default.id,
            }
        )

        self.move_line = self.env["stock.move.line"].create(
            {
                "product_id": self.product.id,
                "lot_id": self.lot.id,
                "company_id": self.env.company.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location_dest.id,
                "move_id": self.move.id,
                "picking_id": self.picking_default.id,
            }
        )

    def test_open_lot_form_action(self):
        action = self.move_line.action_open_lot_form()
        self.assertIsInstance(action, dict)
        self.assertEqual(action.get("type"), "ir.actions.act_window")
        self.assertEqual(action.get("res_model"), "stock.lot")
        self.assertEqual(action.get("res_id"), self.lot.id)
        self.assertEqual(action.get("view_mode"), "form")
        self.assertEqual(self.product.tracking, "lot")

    def test_open_lot_form_action_without_lot_id(self):
        move_line_no_lot = self.env["stock.move.line"].create(
            {
                "product_id": self.product.id,
                "company_id": self.env.company.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location_dest.id,
                "move_id": self.move.id,
                "lot_id": False,
            }
        )
        with self.assertRaises(UserError):
            move_line_no_lot.action_open_lot_form()

    def test_compute_show_lot_button(self):
        self.move.picking_id = self.picking_default
        self.move_line.picking_id = self.picking_default
        self.move_line._compute_show_lot_button()
        self.assertTrue(self.move_line.show_lot_button)

    def test_open_lot_form_action_with_popup(self):
        self.move.picking_id = self.picking_popup
        self.move_line.picking_id = self.picking_popup
        action = self.move_line.action_open_lot_form()
        self.assertEqual(action.get("target"), "new")
        self.assertEqual(action.get("view_mode"), "form")
        self.assertEqual(action.get("res_model"), "stock.lot")
        self.assertEqual(action.get("res_id"), self.lot.id)
