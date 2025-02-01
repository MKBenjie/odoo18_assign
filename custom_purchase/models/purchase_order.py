# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(
        'res.partner', 
        string='Vendor', 
        required=True, 
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
    
    # def action_close_bid(self):
    #     """Updates state to 'Bid Closed' when the bidding process is done."""
    #     self.write({'state': 'bid_closed'})

    @api.onchange('vendor_ids')
    def _onchange_vendor_ids(self):
        """
        Automatically set the first vendor in the list to the `partner_id` field
        if no vendor has been selected.
        """
        if not self.partner_id and self.vendor_ids:
            self.partner_id = self.vendor_ids[0]

    @api.model_create_multi
    def create(self, vals_list):
        """
        Ensure a vendor is selected or set the first vendor automatically.
        """
        for vals in vals_list:
            # Check if 'vendor_ids' is in the correct format
            vendor_ids = vals.get('vendor_ids')
            # print("These are the Vendor IDS", vendor_ids)
            # print("These are the Vendor IDS", vals['partner_id'])
            if vendor_ids and isinstance(vendor_ids, list):
                # vendor_ids = vendor_ids[0][2]  # Extract the list of vendor IDs
                if vendor_ids and not vals.get('partner_id'):
                    vals['partner_id'] = vendor_ids[0]  # Set the first vendor as the default

            if not vals.get('partner_id'):
                # Fetch the first available vendor from the system
                default_vendor = self.env['res.partner'].search([('supplier_rank', '>', 0)], limit=1)

                if default_vendor:
                    vals['partner_id'] = default_vendor.id  # Assign the default vendor
                else:
                    raise UserError("A vendor must be selected, but no vendors exist in the system.")
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

