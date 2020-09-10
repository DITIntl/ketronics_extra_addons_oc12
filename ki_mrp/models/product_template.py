from odoo import fields, api, models
from datetime import datetime
from odoo import tools
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ProductTemplate(models.Model):
    _inherit = "product.template"

    _sql_constraints = [
        ('default_code_uniq', 'unique (default_code)',
         'The Internal Reference of the product must be unique!')
    ]

    # list_price = fields.Float(string="Sales Price", digits=(12, 4))
    # standard_price = fields.Float(string="Cost", digits=(12, 4))
