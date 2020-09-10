from odoo import fields, api, models
from datetime import datetime
from odoo import tools
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    #product_qty = fields.Float(digits=(4, 4))
