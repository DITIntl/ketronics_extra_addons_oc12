from odoo import fields, api, models


class sale_order_line(models.Model):
    _inherit = "purchase.order.line"

    qty_balance = fields.Float(
        string="Balance Qty", readonly=True, compute="compute_qty_balance")
    # price_unit = fields.Float(string="Unit Price", digits=(12, 4))

    @api.depends('product_qty', 'qty_received')
    def compute_qty_balance(self):
        for row in self:
            row.qty_balance = row.product_qty - row.qty_received
