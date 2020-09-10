# -*- coding: utf-8 -*-
{
    'name': "Custom",

    'summary': """
        Custom modules""",

    'description': """
        Custom modules
    """,

    'author': "Team",
    'website': "http://www.kikinsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': False
}
