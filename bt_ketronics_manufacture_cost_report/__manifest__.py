# -*- coding: utf-8 -*-
{
    'name': "CoGM PT Ketronics Indonesia",

    'summary': """
        Cost of Goods Manufactured Report PT. Ketronics Indonesia""",

    'description': """
        Cost of Goods Manufactured Report PT. Ketronics Indonesia
    """,

    'author': "butirpadi@gmail.com",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacture',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_default_data.xml',
        'views/mc_report_config_view.xml',
        'views/mc_report_wizard_view.xml',
        'reports/mc_report_template.xml',
        'reports/action_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}
