from odoo import models, fields


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one(
        comodel_name='purchase.request',
        string='Purchase Request',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    product_qty = fields.Float(string='Quantity', required=True, default=1.0)
    description = fields.Text(string='Description')