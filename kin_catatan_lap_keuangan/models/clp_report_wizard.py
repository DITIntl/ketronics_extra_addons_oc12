from odoo import api, fields, models, _
from pprint import pprint
from datetime import *
from odoo.exceptions import UserError


class CLPReportWizard(models.TransientModel):
    _name = 'clp.report.wizard'

    name = fields.Char(string='Name', default="Catatan Laporan Keuangan")
    date_from = fields.Date(string="Date start")
    date_to = fields.Date(string="Date to")
    report_config_id = fields.Many2one(
        'clp.report.config', string='CLP Config')

    def get_report_data(self):
        sales_cost = 0
        general_cost = 0
        other_income = 0
        other_cost = 0

        report_config = self.env.ref(
            'kin_catatan_lap_keuangan.clp_report_config_default')

        # ----------------------------------------------------------------------------------------
        # get sales cost
        sales_cost_accounts = report_config.sales_cost_account_ids
        sales_cost = {}
        sales_cost_value = 0

        sales_cost_aml = self.env['account.move.line'].search([
            ('account_id', 'in', sales_cost_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        sales_cost_aml = sales_cost_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        sales_cost_value = abs(sum(sales_cost_aml.mapped('balance')))

        for acc in sales_cost_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if(total_amls > 0):
                sales_cost[acc] = total_amls

        # ----------------------------------------------------------------------------------------
        # get general cost
        general_cost_accounts = report_config.general_cost_account_ids
        general_cost = {}
        general_cost_value = 0

        general_cost_aml = self.env['account.move.line'].search([
            ('account_id', 'in', general_cost_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        general_cost_aml = general_cost_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        general_cost_value = abs(sum(general_cost_aml.mapped('balance')))

        for acc in general_cost_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            # total_amls = abs(sum(acc_amls.mapped('debit')) -
            #                  sum(acc_amls.mapped('credit')))
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if(total_amls > 0):
                general_cost[acc] = total_amls

        # ----------------------------------------------------------------------------------------
        # get other income
        other_income_accounts = report_config.other_income_account_ids
        other_income = {}
        other_income_value = 0

        other_income_aml = self.env['account.move.line'].search([
            ('account_id', 'in', other_income_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        other_income_aml = other_income_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        other_income_value = abs(sum(other_income_aml.mapped('balance')))

        for acc in other_income_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            # total_amls = abs(sum(acc_amls.mapped('debit')) -
            #                  sum(acc_amls.mapped('credit')))
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if (total_amls > 0):
                other_income[acc] = total_amls

        # ----------------------------------------------------------------------------------------
        # get other cost
        other_cost_accounts = report_config.other_cost_account_ids
        other_cost = {}
        other_cost_value = 0

        other_cost_aml = self.env['account.move.line'].search([
            ('account_id', 'in', other_cost_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        other_cost_aml = other_cost_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        other_cost_value = abs(sum(other_cost_aml.mapped('balance')))

        for acc in other_cost_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            # total_amls = abs(sum(acc_amls.mapped('debit')) -
            #                  sum(acc_amls.mapped('credit')))
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if (total_amls > 0):
                other_cost[acc] = total_amls

        report_data = {
            'sales_cost': sales_cost,
            'general_cost': general_cost,
            'other_income': other_income,
            'other_cost': other_cost,
        }

        # raise UserError('Mohon maaf tidak bisa ..')
        return report_data

    def action_submit(self):
        return self.env.ref('kin_catatan_lap_keuangan.clp_report_action').report_action(self)
