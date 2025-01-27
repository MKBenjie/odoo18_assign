# -*- coding: utf-8 -*-
import base64
from odoo import http
from odoo.http import request


class NationalApplicantController(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kwargs):
        return request.render('id_application.national_application_homepage', {})

    @http.route('/national_id/status', type='http', auth='public', website=True)
    def application_status(self, **kwargs):
        return request.render('id_application.application_status_template', {})

    @http.route('/national_id/track', type='http', auth='public', website=True, csrf=True)
    def track_application(self, reference=None):
        if reference:
            applicant = request.env['national.applicant'].sudo().search([('reference', '=', reference)], limit=1)
            if applicant:
                return request.render('id_application.tracking_result_template', {
                    'applicant': applicant
                })
            else:
                return request.render('id_application.tracking_result_template', {
                    'error': 'No application found with this reference number.'
                })
        return request.render('id_application.tracking_form_template')

    @http.route('/national_id/apply', type='http', auth='public', website=True)
    def application_form(self, **kwargs):
        return request.render('id_application.application_form_template', {})

    @http.route('/national_id/submit', type='http', auth='public', website=True, csrf=True)
    def submit_application(self, **kwargs):
        # Extract form data
        first_name = kwargs.get('first_name')
        sur_name = kwargs.get('sur_name')
        other_name = kwargs.get('other_name')
        gender = kwargs.get('gender')
        address = kwargs.get('address')
        dob = kwargs.get('dob')

        # Handle uploaded files
        photo = kwargs.get('photo')  # Uploaded photo
        lc_letter = kwargs.get('lc_letter')  # Uploaded LC letter

        # Ensure required fields are provided
        if not first_name or not sur_name or not gender or not address or not dob or not photo or not lc_letter:
            return request.render('id_application.error_template', {
                'error_message': "Please ensure all required fields are filled and files are uploaded.",
            })

        if not photo.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            return request.render('id_applicant.error_template',
                              {'error_message': "Invalid photo file format. Please upload a JPEG or PNG image."})
        if not lc_letter.filename.lower().endswith(('.pdf')):
            return request.render('id_applicant.error_template',
                                {'error_message': "Invalid LC Letter file format. Please upload a PDF document."})

        try:
            # Create new applicant record
            applicant = request.env['national.applicant'].sudo().create({
                'first_name': first_name,
                'sur_name': sur_name,
                'other_name': other_name,
                'gender': gender,
                'address': address,
                'dob': dob,
                'stage': 'sent',  # Set stage to 'Sent'
                'photo': base64.b64encode(photo.read()),
                'file_name': photo.filename,
                'lc_letter': base64.b64encode(lc_letter.stream.read()),
            })
        except Exception as e:
            return request.render('id_application.error_template', {
                'error_message': f"An error occurred while saving your application: {str(e)}",
            })

        # Redirect to the success page with the reference number
        return request.render('id_application.success_page_template', {
            'reference': applicant.reference
        })

    @http.route('/national_id/success', type='http', auth='public', website=True)
    def success_page(self, **kwargs):
        return request.render('id_application.success_page_template', {})