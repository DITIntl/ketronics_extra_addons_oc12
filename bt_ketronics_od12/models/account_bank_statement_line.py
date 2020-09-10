from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    no_bpk = fields.Char(string="Nomor BPK", required=False, )
