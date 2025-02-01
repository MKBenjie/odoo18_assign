from odoo import http
from odoo.http import request

class VendorPortalController(http.Controller):

    @http.route('/my/requests', website=True, auth='public', type='http')
    def view_requests(self):
        """
        Fetch and display all vendor requests assigned to the logged-in vendor.
        """
        vendor = request.env.user.partner_id
        print(f"Logged-in Vendor ID: {vendor.id}")
        sent_requests = request.env['purchase.order'].search([
            ('bid_state', '=', 'vendor_requests_sent'),
            ('vendor_ids', 'in', vendor.id)
        ])
        return request.render('custom_purchase.portal_request_list_view_template', {
            'requests': sent_requests,
        })

    @http.route('/my/requests/<int:request_id>/submit_bid', type='http', auth='public', website=True)
    def submit_bid_form(self, request_id):
        """
        Display the bid submission form for a specific vendor request.
        """
        rfq = request.env['purchase.order'].search([('id', '=', request_id)])
        # print("Purchace order........", rfq.name)
        # print("Order Line .........", rfq.order_line)
        # for line in rfq.order_line:
        #     print(line.product_id.id)

        return request.render('custom_purchase.vendor_submit_bid_template', {
            'rfq': rfq,
            'order_lines': rfq.order_line
        })

    @http.route('/my/requests/<int:request_id>/submit_bid', type='http', auth='public', website=True, methods=['POST'])
    def submit_bid(self, request_id, **post):
        rfq = request.env['purchase.order'].browse(request_id)
        vendor = request.env.user.partner_id

        if vendor not in rfq.vendor_ids:
            return request.redirect('/my/requests')  # Redirect if vendor is unauthorized

        # 🔹 Check if the vendor has already submitted a bid
        existing_bid = request.env['purchase.order.bid'].search([
            ('rfq_id', '=', rfq.id),
            ('vendor_id', '=', vendor.id)], limit=1)

        if existing_bid:
            return request.redirect('/my/home')

        # 🔹 Retrieve form data
        bid_amount = post.get('bid_amount')
        bid_notes = post.get('note')

        # 🔹 Create bid record
        bid = request.env['purchase.order.bid'] .create({
            'rfq_id': rfq.id,
            'vendor_id': vendor.id,
            'bid_amount': float(bid_amount),
            'bid_notes': bid_notes,
        })
        if not bid:
            print("I haven't received anything for the model")

        return request.redirect('/my/requests')