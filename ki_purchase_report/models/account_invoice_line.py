from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    efaktur_masukan = fields.Char(
        related='invoice_id.efaktur_masukan', string='NSFP', store=True)
