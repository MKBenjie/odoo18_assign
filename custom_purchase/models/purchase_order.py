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

    bid_ids = fields.One2many(
        comodel_name='purchase.order.bid',
        inverse_name='rfq_id',
        string='Bids',
        help="Bids received in response to this RFQ."
    )

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
            if vendor_ids and isinstance(vendor_ids, list) and vendor_ids[0][0] == 6:
                vendor_ids = vendor_ids[0][2]  # Extract the list of vendor IDs
                if vendor_ids and not vals.get('partner_id'):
                    vals['partner_id'] = vendor_ids[0]  # Set the first vendor as the default
        return super(CustomPurchaseOrder, self).create(vals_list)

    def action_rfq_send(self):
        """
        Customize the 'Send by Email' functionality to include all vendors in the 'To' field.
        """
        self.ensure_one()  # Ensure the method is called on a single record
        template = self.env.ref('purchase.email_template_edi_purchase', raise_if_not_found=False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', raise_if_not_found=False)

        # Fetch vendors' partner IDs
        partner_ids = self.vendor_ids.ids if self.vendor_ids else ([self.partner_id.id] if self.partner_id else [])
        if not partner_ids:
            raise UserError("Please ensure at least one vendor is selected.")


        ctx = {
            'default_model': 'purchase.order',
            'default_res_ids': [self.id],
            'default_partner_ids': partner_ids,  # Add vendors to the recipients
            'default_template_id': template.id if template else False,
            'default_use_template': bool(template),
            'default_composition_mode': 'comment'
        }

        # Explicitly mark as sent
        self.write({'state': 'sent'})  # Updates the record's state to 'sent'

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }