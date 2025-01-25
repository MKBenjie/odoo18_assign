from odoo import models, fields, api


class PurchaseRFQVendor(models.Model):
    _name = 'purchase.rfq.vendor'
    _description = 'RFQ Vendor Line'

    partner_id = fields.Many2one('res.partner', domain=[('supplier', '=', True)], string='Vendor', required=True)
    order_id = fields.Many2one('purchase.order', string='RFQ', required=True, ondelete='cascade')