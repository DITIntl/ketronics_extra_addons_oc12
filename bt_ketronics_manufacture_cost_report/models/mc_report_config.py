from odoo import api, fields, models


class MCReportConfig(models.Model):
    _name = 'mc.report.config'
    _description = 'Manufacture Cost Report'

    name = fields.Char(string='Name', default="Manufacture Cost Report")
    property_valuation = fields.Selection([("manual", "Manual (Periodic)"), (
        "real_time", "Automatic (Perpetual)")], string='Inventory Valuation')
    stock_journal_id = fields.Many2one(
        string='Jurnal Persediaan',
        comodel_name='account.journal',
        ondelete='restrict',
    )
    purchase_journal_id = fields.Many2one(
        string='Jurnal Pembelian',
        comodel_name='account.journal',
        ondelete='restrict',
    )
    adjustment_journal_id = fields.Many2one(
        string='Jurnal Penyesuaian',
        comodel_name='account.journal',
        ondelete='restrict',
    )

    stock_input_account_id = fields.Many2one(
        string='Stock Input Account',
        comodel_name='account.account',
        ondelete='restrict',
    )
    pembelian_material_account_id = fields.Many2one(
        string='Akun Pembelian Material',
        comodel_name='account.account',
        ondelete='restrict',
    )
    manual_persediaan_material_account_id = fields.Many2one(
        string='Akun Persediaan Material',
        comodel_name='account.account',
        ondelete='restrict',
    )
    realtime_persediaan_material_account_id = fields.Many2one(
        string='Akun Persediaan Material',
        comodel_name='account.account',
        ondelete='restrict',
    )
    persediaan_barang_dalam_proses_account_id = fields.Many2one(
        string='Akun Persediaan Dalam Proses',
        comodel_name='account.account',
        ondelete='restrict',
    )
    persediaan_barang_jadi_account_id = fields.Many2one(
        string='Akun Persediaan Barang Jadi',
        comodel_name='account.account',
        ondelete='restrict',
    )
    labor_cost_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='mc_report_labor_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Tenaga Kerja'
    )
    overhead_cost_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='mc_report_overhead_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Overhead Pabrik'
    )
    raw_material_product_ids = fields.Many2many(
        comodel_name='product.product',
        relation='mc_report_raw_material_product_template_rel',
        column1='report_id',
        column2='product_id',
        string='Bahan Baku'
    )
    component_product_ids = fields.Many2many(
        comodel_name='product.product',
        relation='mc_report_component_product_template_rel',
        column1='report_id',
        column2='product_id',
        string='Bahan Penolong'
    )
    pembelian_material_account_ids = fields.Many2many(
        comodel_name='account.account',
        relation='mc_report_purchase_cost_account_account_rel',
        column1='report_id',
        column2='account_id',
        string='Akun Biaya Pembelian'
    )

    def execute(self):
        print('Execute Function')
