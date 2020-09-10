from odoo import api, fields, models


class CLPReportConfig(models.Model):
    _name = 'clp.report.config'
    _description = 'Catatan Laporan Keuangan'

    name = fields.Char(string='Name', default="Catatan Laporan Keuangan")
    sales_cost_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='clp_sales_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Penjualan'
    )
    general_cost_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='clp_general_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Administrasi & Umum'
    )
    other_income_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='clp_other_income_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Penjualan'
    )
    other_cost_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='clp_report_other_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Lain-lain'
    )

    def execute(self):
        print('Execute Function')
