# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import api, fields, models

from odoo.addons.queue_job.job import DONE, job


class StockPicking(models.Model):
    _inherit = "stock.picking"

    picking_queue_ids = fields.Many2many(
        string="Picking Queues",
        comodel_name="queue.job",
        compute="_compute_picking_queues",
        copy=False,
    )
    has_queues = fields.Boolean(
        string="Has Queues", readonly=True, compute="_compute_has_queues"
    )
    created = fields.Boolean(string="created")

    @api.multi
    def _compute_picking_queues(self):
        for sel in self:
            all_queues = self.env["queue.job"].search(
                [
                    ("model_name", "=", "stock.picking"),
                ]
            )
            sel.picking_queue_ids = all_queues.filtered(
                lambda a: sel.id in a.record_ids
            ).ids

    @api.depends("picking_queue_ids")
    def _compute_has_queues(self):
        for sel in self:
            sel.has_queues = True if sel.picking_queue_ids else False

    @api.multi
    def button_validate(self):
        return_values = super(StockPicking, self).button_validate()
        self.set_queues_to_done("Set to done when validating picking.")
        return return_values

    @api.multi
    def write(self, vals):
        return_value = super(StockPicking, self).write(vals)
        # no se hace el for sel in self porque en el super tampoc se hace
        for sel in self:
            # Se comprueban las notificacions que utilizan carrier_id como campo vacío
            if sel.carrier_id or vals.get("carrier_id"):
                sel.set_queues_to_done(
                    "Set to done when selecting carrier", "carrier_id"
                )
            elif not sel.purchase_shipping_date and not vals.get(
                "purchase_shipping_date"
            ):
                sel.set_queues_to_done(
                    "Set to done when removing shipping date", "carrier_id"
                )
            if (
                sel.purchase_id
                and not sel.carrier_id
                and not vals.get("carrier_id")
                and sel.state not in ["done", "cancel", "draft"]
            ):
                sel.set_queues_to_done(
                    "Set to done when selecting shipping date", "carrier_id"
                )
                sel.picking_notify_carrier()

            # Se comprueban las notificacions que utilizan purchase_shipping_date como campo vacío
            if sel.purchase_shipping_date or vals.get("purchase_shipping_date"):
                sel.set_queues_to_done(
                    "Set to done when selecting purchase shipping date", "shipping_date"
                )
            if (
                sel.purchase_id
                and not sel.purchase_shipping_date
                and not vals.get("purchase_shipping_date")
                and sel.state not in ["done", "cancel", "draft"]
            ):
                sel.set_queues_to_done(
                    "Set to done when selecting shipping date", "shipping_date"
                )
                sel.picking_notify_shipping_date()
        return return_value

    @api.multi
    def action_cancel(self):
        return_values = super(StockPicking, self).action_cancel()
        self.set_queues_to_done("Set to done when cancelling picking")
        return return_values

    @api.multi
    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()
        for sel in self:
            if sel.state == "assigned":
                sel.set_queues_to_done("Set to done when confirming picking")
                if not sel.carrier_id:
                    sel.picking_notify_carrier()
                if not sel.purchase_shipping_date:
                    sel.picking_notify_shipping_date()
        return res

    # Se crean las notificacions que utilizan carrier_id como campo vacío
    @api.multi
    def picking_notify_carrier(self):
        for sel in self.filtered(
            lambda a: a.state not in ["draft", "done", "cancel", "waiting"]
        ):
            if sel.picking_type_id.code == "incoming" and sel.purchase_id:
                order_type = sel.purchase_id.order_type
                date_now = datetime.now()
                for mail in order_type.picking_mail_notify_ids.filtered(
                    lambda a: a.empty_field == "carrier_id"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        mail.reference_field, mail.notify_when, mail.notify_time
                    )
                    if triggering_date and triggering_date > date_now:
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_mail_notify_carrier(mail)
                for log in order_type.picking_log_note_notify_ids.filtered(
                    lambda a: a.empty_field == "carrier_id"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        log.reference_field, log.notify_when, log.notify_time
                    )
                    if triggering_date and triggering_date > date_now:
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_log_notify_carrier(log)
                for activity in order_type.picking_activity_notify_ids.filtered(
                    lambda a: a.empty_field == "carrier_id"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        activity.reference_field,
                        activity.notify_when,
                        activity.notify_time,
                    )
                    if triggering_date and triggering_date > date_now:
                        # Le paso el triggering date para utilizarlo como referencia
                        # para hacer la acción planificada
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_activity_notify_carrier(
                            activity, triggering_date
                        )

    # Se crean las notificacions que utilizan purchase_shipping_date como campo vacío
    @api.multi
    def picking_notify_shipping_date(self):
        for sel in self.filtered(
            lambda a: a.state not in ["draft", "done", "cancel", "waiting"]
        ):
            if sel.picking_type_id.code == "incoming" and sel.purchase_id:
                order_type = sel.purchase_id.order_type
                date_now = datetime.now()
                for mail in order_type.picking_mail_notify_ids.filtered(
                    lambda a: a.empty_field == "purchase_shipping_date"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        mail.reference_field, mail.notify_when, mail.notify_time
                    )
                    if triggering_date and triggering_date > date_now:
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_mail_notify_shipping_date(mail)
                for log in order_type.picking_log_note_notify_ids.filtered(
                    lambda a: a.empty_field == "purchase_shipping_date"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        log.reference_field, log.notify_when, log.notify_time
                    )
                    if triggering_date and triggering_date > date_now:
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_log_notify_shipping_date(log)
                for activity in order_type.picking_activity_notify_ids.filtered(
                    lambda a: a.empty_field == "purchase_shipping_date"
                ):
                    triggering_date = sel.calculate_trigger_time(
                        activity.reference_field,
                        activity.notify_when,
                        activity.notify_time,
                    )
                    if triggering_date and triggering_date > date_now:
                        # Le paso el triggering date para utilizarlo como referencia
                        # para hacer la acción planificada
                        sel.with_delay(
                            eta=triggering_date
                        ).delay_picking_activity_notify_shipping_date(
                            activity, triggering_date
                        )

    @job(default_channel="root.picking_notify_carrier")
    def delay_picking_mail_notify_carrier(self, mail):
        if not self.carrier_id and self.state == "assigned":
            self.message_post_with_template(mail.mail_template_id.id)

    @job(default_channel="root.picking_notify_carrier")
    def delay_picking_log_notify_carrier(self, log):
        if not self.carrier_id and self.state == "assigned":
            self.env["mail.message"].create(
                {
                    "body": log.note_text,
                    "model": "stock.picking",
                    "res_id": self.id,
                    "message_type": "comment",
                    "subtype_id": self.env.ref("mail.mt_note").id,
                }
            )

    @job(default_channel="root.picking_notify_carrier")
    def delay_picking_activity_notify_carrier(self, activity, triggering_date):
        if not self.carrier_id and self.state == "assigned":
            deadline = fields.Datetime.to_string(
                triggering_date + timedelta(days=activity.time_to_deadline)
            )
            self.env["mail.activity"].create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "date_deadline": deadline,
                    "summary": activity.summary,
                    "note": activity.note,
                    "user_id": activity.user_id.id,
                    "res_id": self.id,
                    "res_model_id": self.env["ir.model"]
                    .search([("model", "=", "stock.picking")], limit=1)
                    .id,
                }
            )

    @job(default_channel="root.picking_notify_shipping_date")
    def delay_picking_mail_notify_shipping_date(self, mail):
        if not self.purchase_shipping_date and self.state == "assigned":
            self.message_post_with_template(mail.mail_template_id.id)

    @job(default_channel="root.picking_notify_shipping_date")
    def delay_picking_log_notify_shipping_date(self, log):
        if not self.purchase_shipping_date and self.state == "assigned":
            self.env["mail.message"].create(
                {
                    "body": log.note_text,
                    "model": "stock.picking",
                    "res_id": self.id,
                    "message_type": "comment",
                    "subtype_id": self.env.ref("mail.mt_note").id,
                }
            )

    @job(default_channel="root.picking_notify_shipping_date")
    def delay_picking_activity_notify_shipping_date(self, activity, triggering_date):
        if not self.purchase_shipping_date and self.state == "assigned":
            deadline = fields.Datetime.to_string(
                triggering_date + timedelta(days=activity.time_to_deadline)
            )
            self.env["mail.activity"].create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "date_deadline": deadline,
                    "summary": activity.summary,
                    "note": activity.note,
                    "user_id": activity.user_id.id,
                    "res_id": self.id,
                    "res_model_id": self.env["ir.model"]
                    .search([("model", "=", "stock.picking")], limit=1)
                    .id,
                }
            )

    @api.multi
    def set_queues_to_done(self, message, field=False):
        for sel in self:
            if field:
                channel = (
                    "root.picking_notify_carrier"
                    if field == "carrier_id"
                    else "root.picking_notify_shipping_date"
                )
                for notification in sel.picking_queue_ids.filtered(
                    lambda a: a.state not in ["done"] and a.channel == channel
                ):
                    notification._change_job_state(DONE, message)
            else:
                for notification in sel.picking_queue_ids.filtered(
                    lambda a: a.state not in ["done"]
                ):
                    notification._change_job_state(DONE, message)

    def calculate_trigger_time(self, reference, when, time):
        triggering_date = (
            self.scheduled_date
            if reference == "scheduled_date"
            else self.purchase_shipping_date
        )
        if when == "before" and triggering_date:
            triggering_date -= timedelta(hours=time)
        if when == "after" and triggering_date:
            triggering_date += timedelta(hours=time)
        return triggering_date

    def cancell_all_jobs(self):
        for sel in self:
            sel.set_queues_to_done("Set to done manually")

    def redo_jobs(self):
        for sel in self:
            sel.set_queues_to_done("Set to done when redoing jobs")
            if not self.carrier_id:
                self.picking_notify_carrier()
            if not self.purchase_shipping_date:
                self.picking_notify_shipping_date()
