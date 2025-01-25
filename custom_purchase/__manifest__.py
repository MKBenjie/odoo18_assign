# -*- coding: utf-8 -*-
{
    'name': "Custom Purchase App",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/purchase_views.xml',
        'views/purchase_order_view.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}

