# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class bt_ketronics_manufacture_cost_report(models.Model):
#     _name = 'bt_ketronics_manufacture_cost_report.bt_ketronics_manufacture_cost_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100