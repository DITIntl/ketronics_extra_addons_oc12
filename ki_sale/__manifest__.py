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
    'category': 'Sales Management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management','bt_ketronics_sales_report','report_xlsx'],

    # always loaded
    'data': [
        'views/sale_order.xml',
        'views/res_partner_views.xml',
        'views/sales_report_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': False
}
