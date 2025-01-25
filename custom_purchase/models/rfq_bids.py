from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrderBid(models.Model):
    _name = 'purchase.order.bid'
    _description = 'Purchase Order Bid'

    rfq_id = fields.Many2one(
        comodel_name='purchase.order',
        string='RFQ',
        required=True,
        ondelete='cascade',
        help="The RFQ associated with this bid."
    )
    vendor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Vendor',
        required=True,
        help="The vendor who submitted this bid."
    )
    bid_amount = fields.Monetary(
        string='Bid Amount',
        required=True,
        currency_field='currency_id',
        help="The bid amount offered by the vendor."
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='rfq_id.currency_id',
        readonly=True,
        help="Currency of the bid amount."
    )
    bid_notes = fields.Text(string='Notes', help="Additional notes or terms from the vendor.")
    bid_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string='Attachments',
        help="Attachments provided with the bid."
    )


    @api.constrains('vendor_id')
    def _check_vendor_validity(self):
        """
        Ensure the vendor is part of the RFQ's vendors.
        """
        for record in self:
            if record.vendor_id not in record.rfq_id.vendor_ids:
                raise ValidationError("The vendor is not associated with the RFQ.")

    @api.model_create_multi
    def create(self, vals_list):
        bids = []
        for vals in vals_list:
            rfq = self.env['purchase.order'].browse(vals.get('rfq_id'))
            if vals.get('vendor_id') not in rfq.vendor_ids.ids:
                raise ValidationError("The vendor is not associated with the RFQ.")
            bids.append(super(PurchaseOrderBid, self).create(vals))
        return bids
