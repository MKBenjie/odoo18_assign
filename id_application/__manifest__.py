# -*- coding: utf-8 -*-
{
    "name": "NIA",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "Mugagga Benjamin",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "web"],
    "assets": {
        "web.assets_backend": [
            'web/static/lib/owl/owl.js',
            "id_application/static/src/js/apply_button.js",
            "id_application/static/src/css/button_status.css",
        ],
        "web.assets_frontend": [
            "id_application/static/src/css/customized_list.css",
        ],
    },
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/view_denial_reason_form.xml",
        "views/applicant_template.xml",
        "views/application_request_views.xml",
        "views/application_views.xml",
        "views/menu.xml",
    ],
    "license": "LGPL-3",
}
