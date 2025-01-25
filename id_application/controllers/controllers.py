# -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request


# class IdApplication(http.Controller):
#     @http.route('/id_application/id_application', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/id_application/id_application/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('id_application.listing', {
#             'root': '/id_application/id_application',
#             'objects': http.request.env['id_application.id_application'].search([]),
#         })

#     @http.route('/id_application/id_application/objects/<model("id_application.id_application"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('id_application.object', {
#             'object': obj
#         })

