from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # _sql_constraints = [
    #     ('default_code_uniq', 'unique (default_code)',
    #      'The Internal Reference of the product must be unique!')
    # ]
    qty_per_pack = fields.Integer('Qty/Pack', default=1)
    pack_weight = fields.Float('Pack Weight')
