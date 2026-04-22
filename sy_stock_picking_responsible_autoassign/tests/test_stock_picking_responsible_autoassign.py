# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestStockPickingResponsibleAutoassign(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.picking_type = cls.env.ref("stock.picking_type_out")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test customer",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "type": "consu",
            }
        )
        cls.other_user = cls.env.ref("base.user_admin")

    def _create_picking(self, user=False):
        return self.env["stock.picking"].create(
            {
                "partner_id": self.partner.id,
                "picking_type_id": self.picking_type.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "user_id": user.id if user else False,
                "move_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.display_name,
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "product_uom": self.product.uom_id.id,
                            "location_id": self.stock_location.id,
                            "location_dest_id": self.customer_location.id,
                        },
                    )
                ],
            }
        )

    def test_assign_responsible_on_validate(self):
        self.picking_type.assign_responsible_on_validate = True
        picking = self._create_picking()
        self.assertFalse(picking.user_id)
        picking.action_confirm()
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.quantity = move_line.move_id.product_uom_qty
        picking.with_context(skip_immediate=True, skip_backorder=True).button_validate()
        self.assertEqual(picking.user_id, self.env.user)

    def test_do_not_override_existing_responsible(self):
        self.picking_type.assign_responsible_on_validate = True
        picking = self._create_picking(user=self.other_user)
        self.assertEqual(picking.user_id, self.other_user)
        picking.action_confirm()
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.quantity = move_line.move_id.product_uom_qty
        picking.with_context(skip_immediate=True, skip_backorder=True).button_validate()
        self.assertEqual(picking.user_id, self.other_user)
