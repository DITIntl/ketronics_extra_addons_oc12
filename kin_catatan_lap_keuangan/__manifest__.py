# -*- coding: utf-8 -*-
{
    'name': "Catatan Laporan Keuangan",

    'summary': """
        Catatan laporan keuangan terdiri dari biaya-biaya dan penghasilan dari luar usaha""",

    'description': """
        Catatan laporan keuangan terdiri dari:
         1. biaya penjualan
         2. biaya administrasi & umum 
         3. penghasilan dari luar usaha
         4. biaya lain-lain
    """,

    'author': "Kinsoft Indonesia, Kikin Kusumah",
    'website': "http://kinsoft.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_default_data.xml',
        'views/clp_report_config_view.xml',
        'views/clp_report_wizard_view.xml',
        'reports/clp_report_template.xml',
        'reports/action_report.xml',
    ],
    'installable': True,
    'application': True
}
