from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _description = "Purchase Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Request Number", required=True, default="New", readonly=True
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Requested By",
        required=True,
        default=lambda self: self.env.user.employee_id,
    )
    department_id = fields.Many2one(
        comodel_name="hr.department",
        string="Department",
        required=True,
    )
    date_requested = fields.Date(
        string="Date Requested", default=fields.Date.today, readonly=True
    )
    description = fields.Text(string="Description")
    request_line_ids = fields.One2many(
        comodel_name="purchase.request.line",
        inverse_name="request_id",
        string="Request Lines",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("rfq_created", "RFQ Created"),
        ],
        string="State",
        default="draft",
        tracking=True,
    )

    def action_submit(self):
        """Submit the purchase request to the Procurement Department."""
        self.write({"state": "submitted"})
        return True

    def action_approve(self):
        """Approve the purchase request."""
        self.write({"state": "approved"})
        return True

    def action_reject(self):
        """Reject the purchase request."""
        self.write({"state": "rejected"})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "purchase.request"
                )
        return super(PurchaseRequest, self).create(vals)

    def action_create_rfq(self):
        """Convert a purchase request into an RFQ"""
        PurchaseOrder = self.env['purchase.order']
        order_vals = {
            'origin': self.name,
            'partner_id': False,  # Vendor will be selected later
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'name': line.product_id.name,
                'date_planned': fields.Date.today(),
                'price_unit': 0.0,
            }) for line in self.request_line_ids],
        }
        rfq = PurchaseOrder.create(order_vals)
        self.write({'state': 'rfq_created'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': rfq.id,
            'target': 'current',
        }
