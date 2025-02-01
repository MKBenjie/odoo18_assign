# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(
        'res.partner', 
        string='Vendor', 
        required=False, 
        domain="[('id', 'in', vendor_ids)]",
        help="The selected vendor for this RFQ. Vendors are obtained from the Vendors list."
    )

    vendor_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='purchase_order_res_partner_rel',
        column1='order_id',
        column2='partner_id',
        string='Vendors',
        # domain="[('supplier_rank', '>', 0)]",  # Only suppliers are shown
        help="Select vendors to whom this RFQ is sent"
    )

    request_line_ids = fields.One2many(
        comodel_name='purchase.order.line',  # Link to the order line model
        inverse_name='order_id',  # The field in `purchase.order.line` that links to `purchase.order`
        string="Request Lines"
    )

    bid_ids = fields.One2many(
        comodel_name='purchase.order.bid',
        inverse_name='rfq_id',
        string='Bids',
        help="Bids received in response to this RFQ."
    )
    bid_state = fields.Selection([
        ('draft', 'Draft'),
        ('vendor_requests_sent', 'Vendor Requests Sent'),
        ('bid_closed', 'Bid Closed')
    ], string='State', default='draft', tracking=True)

    def action_send_vendor_requests(self):
        """
        Send vendor requests and change the status to 'Vendor Requests Sent'.
        """
        # self.ensure_one()
        if not self.vendor_ids:
            raise UserError("Please select at least one vendor to send requests.")
        self.write({'bid_state': 'vendor_requests_sent'})
        return True


    @api.model_create_multi
    def create(self, vals_list):
        return super(CustomPurchaseOrder, self).create(vals_list)

    def action_select_winning_bid(self):
        """
        Select the winning bid and update the partner_id.
        """
        self.ensure_one()
        winning_bid = self.bid_ids.filtered(lambda bid: bid.is_winner)
        if not winning_bid:
            raise UserError("Please select a winning bid.")
        self.write({
            'partner_id': winning_bid.vendor_id.id,
            'bid_state': 'bid_closed',
        })
        return True

