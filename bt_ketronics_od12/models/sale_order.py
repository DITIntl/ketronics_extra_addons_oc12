from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manufacture_type = fields.Selection([
        ('in_house', 'In House'),
        ('subcon', 'Subcontract'),
    ], string='Manufacture Type')
