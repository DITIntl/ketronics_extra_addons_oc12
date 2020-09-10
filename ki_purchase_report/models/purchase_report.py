from odoo import api, fields, models


class KinsoftPurchaseReport(models.Model):
    _name = 'kinsoft.purchase.report'

    name = fields.Char(string='Name')
