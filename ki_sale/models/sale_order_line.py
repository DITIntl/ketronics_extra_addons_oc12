from odoo import fields, api, models


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        'SO Date', related='order_id.date_order', readonly=True)
    qty_balance = fields.Float(
        string="Balance Qty", readonly=True, compute="compute_qty_balance")
    # price_unit = fields.Float(string="Unit Price", digits=(12, 4))

    @api.depends('product_uom_qty', 'qty_delivered')
    def compute_qty_balance(self):
        for row in self:
            row.qty_balance = row.product_uom_qty - row.qty_delivered
