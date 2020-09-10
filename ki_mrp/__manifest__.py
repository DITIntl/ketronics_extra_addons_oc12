# -*- coding: utf-8 -*-
{
    'name': "Custom",

    'summary': """
        Custom modul""",

    'description': """
        Custom modul
    """,

    'author': "Team",
    'website': "http://www.kikinsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'views/mrp_production_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': False
}
