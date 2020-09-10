from odoo import fields, api, models


class sale_order_line(models.Model):
    _inherit = "sale.order"

    name = fields.Char(string='Order Reference', required=True, copy=False,
                       readonly=False, index=True)
