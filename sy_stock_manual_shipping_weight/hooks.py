# Copyright 2026 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def pre_init_hook(env):
    openupgrade.update_module_names(
        env.cr,
        [("stock_manual_shipping_weight", "sy_stock_manual_shipping_weight")],
        merge_modules=True,
    )
