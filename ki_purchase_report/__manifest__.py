# -*- coding: utf-8 -*-
{
    'name': "Ketronics Purchase Report",

    'summary': """
        PT. Ketronics Indonesia Custom Module Purchase Report""",

    'description': """
        PT. Ketronics Indonesia Custom Module Purchase Report
    """,

    'author': "butirpadi@gmail.com, kinsoft.indonesia@gmail.com",
    'website': "http://www.kikinsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'account', 'sale_management', 'mrp', 'vit_efaktur', 'bt_ketronics_sales_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # views
        # 'views/res_company_view.xml',
        'views/purchase_report_wizard_view.xml',
        'views/account_invoice_lines.xml',
        # 'views/templates.xml',
        # reports
        'reports/action_report.xml',
        'reports/purchase_report.xml',
        'reports/purchase_report_detail.xml',
        'reports/purchase_report_detail_new.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True
}
