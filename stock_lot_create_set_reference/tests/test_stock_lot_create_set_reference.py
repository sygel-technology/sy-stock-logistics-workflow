# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class SomethingCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_id = cls.env["product.product"].create(
            {"name": "Test Product", "tracking": "serial"}
        )
        cls.receipt_type = cls.env.ref("stock.picking_type_in")
        cls.receipt_type.set_name_internal_ref = True
        picking_form = Form(cls.env["stock.picking"])
        picking_form.picking_type_id = cls.receipt_type
        with picking_form.move_ids_without_package.new() as move_form:
            move_form.product_id = cls.product_id
            move_form.product_uom_qty = 1
        cls.picking_id = picking_form.save()
        cls.picking_id.action_confirm()
        cls.ml_id = cls.picking_id.move_ids_without_package.move_line_ids[:1]

    def test_stock_lot_create_set_reference_button(self):
        """If creating lots with button_validate after setting its names,
        that names should be set in the reference"""
        self.receipt_type.set_name_internal_ref = True
        test_ref = "Test Reference"
        self.ml_id.lot_name = test_ref
        self.picking_id.with_context().button_validate()
        self.assertTrue(self.ml_id.lot_id.name)
        self.assertEqual(self.ml_id.lot_id.ref, test_ref)

    def test_stock_lot_create_set_reference_form(self):
        """If use_existing_lots option, lots are created manually in the form
        setting the name, that name should be set in the reference"""
        self.receipt_type.use_existing_lots = True
        test_ref = "Test Reference"
        self.ml_id.lot_id = (
            self.env["stock.lot"]
            .with_context(active_picking_id=self.picking_id.id)
            .create({"name": test_ref, "product_id": self.ml_id.product_id.id})
        )
        self.assertTrue(self.ml_id.lot_id.name)
        self.assertEqual(self.ml_id.lot_id.ref, test_ref)

    # def test_stock_lot_create_set_reference_autocreate(self):
    #     """ If lots are autocreated, internal ref should not be set """
    #     self.product_id.auto_create_lot = True
    #     self.receipt_type.auto_create_lot = True
    #     self.picking_id.with_context().button_validate()
    #     self.assertTrue(self.ml_id.lot_id.name)
    #     self.assertFalse(self.ml_id.lot_id.ref)
