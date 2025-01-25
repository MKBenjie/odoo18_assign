from odoo import exceptions, models, api, fields, _


class NationalApplicant(models.Model):
    _name = "national.applicant"
    _description = "Applicants Details"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "create_uid"

    reference = fields.Char(string="Reference", default="New", copy=False)
    first_name = fields.Char(string="First Name", required=True, tracking=True)
    sur_name = fields.Char(string="Sur Name", required=True, tracking=True)
    other_name = fields.Char(string="Other Name", tracking=True)
    dob = fields.Date(string="Date of Birth", required=True, tracking=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        string="Gender",
        required=True,
        tracking=True,
    )
    address = fields.Text(string="Address", required=True, tracking=True)
    photo = fields.Image(
        string="Photo",
        max_width=480,
        max_height=480,
        tracking=False,
        required=True,
        copy=False,
    )
    file_name = fields.Char("File name", copy=False)
    lc_letter = fields.Binary(
        string="LC Reference Letter",
        attachment=True,
        tracking=False,
        required=True,
        copy=False,
    )
    stage = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("validating", "Validating"),
            ("approved", "Approved"),
            ("denied", "Denied"),
        ],
        string="Stage",
        default="draft",
        copy=False,
        tracking=True,
    )
    denial_reason = fields.Text(string="Denial Reason", tracking=True, copy=False)

    def open_application_form(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "national.applicant",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref('id_application.view_national_id_applicant_form').id,  # Ensure you reference the correct form view
            "target": "current",
        }
    
    def action_open_denial_modal(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Deny Application"),
            "res_model": "national.applicant",
            "view_mode": "form",
            "view_id": self.env.ref("id_application.view_denial_reason_form").id,
            "target": "new",
            "res_id": self.id,
        }

    def confirm_denial(self):
        """
        Confirm the denial by updating the denial reason and moving the application to the 'denied' stage.
        """
        if self.stage not in ["sent", "validating"]:
            raise exceptions.UserError(
                _("Only applications in the 'Sent' or 'Validating' stages can be denied.")
            )

        if not self.denial_reason:
            raise exceptions.ValidationError(_("Please provide a reason for denial."))

        # Update the stage and log the denial reason
        self.write({
            "stage": "denied",
            "denial_reason": self.denial_reason,
        })

        # Send a notification
        self.message_post(
            body=_("Application denied. Reason: %s") % self.denial_reason,
            subtype_xmlid="mail.mt_comment",
        )
        return True

    def move_to_sent(self):
        if self.stage != "draft":
            raise exceptions.UserError(
                "Only applications in the 'Draft' stage can be sent."
            )
        self.stage = "sent"
        self.message_post(body="Application has been Sent.")
        return True

    def move_to_validating(self):
        if self.stage != "sent":
            raise exceptions.UserError(
                "Only applications in the 'Sent' stage can be moved to 'Validating'."
            )
        self.stage = "validating"
        self.message_post(body="Application is being validated.")
        return True

    def approve_application(self):
        if self.stage != "validating":
            raise exceptions.UserError(
                "Only applications in the 'Validating' stage can be approved."
            )
        self.stage = "approved"
        self.message_post(
            body=_("Congratulations! Your application has been approved.")
        )
        # Notify the applicant
        self.message_post(
            body=_(
                "Dear %(name)s, congratulations! Your application has been approved. Welcome onboard!",
                name=self.first_name or "Applicant",
            ),
            subtype_xmlid="mail.mt_comment",
        )
        return True

    # def deny_application(self):
    #     if self.stage not in ["sent", "validating"]:
    #         raise exceptions.UserError(
    #             "Only applications in the 'Sent' or 'Validating' stages can be denied."
    #         )
    #     self.stage = "denied"
    #     self.message_post(body="Application denied.")
    #     return True

    def confirm_denial(self):
        self.stage = "denied"
        self.message_post(body=_("Application denied."))
        self.message_post(
            body=_(
                "Dear %(name)s, we regret to inform you that your application has been denied. "
                "Reason: %(reason)s",
                name=self.first_name or "Applicant",
                reason=self.denial_reason or _("No reason provided."),
            ),
            subtype_xmlid="mail.mt_comment",
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("reference") or vals["reference"] == "New":
                vals["reference"] = self.env["ir.sequence"].next_by_code(
                    "national.applicant"
                )

        return super(NationalApplicant, self).create(vals_list)
