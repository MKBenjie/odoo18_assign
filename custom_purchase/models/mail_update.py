# from odoo import models

# class MailComposeMessage(models.TransientModel):
#     _inherit = 'mail.compose.message'

#     def send_mail(self, auto_commit=False):
#         """
#         Override send_mail to mark RFQ as sent after sending the email.
#         """
#         res = super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
#         if self._context.get('mark_so_as_sent') and self.env.context.get('default_model') == 'purchase.order':
#             rfq = self.env['purchase.order'].browse(self._context.get('default_res_ids', []))
#             rfq.message_post(body="RFQ sent to vendors.")
#             rfq.write({'state': 'sent'})  # Update the RFQ state to 'sent'
#         return res