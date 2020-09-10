# -*- coding: utf-8 -*-
from odoo import http

# class BtKetronicsManufactureCostReport(http.Controller):
#     @http.route('/bt_ketronics_manufacture_cost_report/bt_ketronics_manufacture_cost_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bt_ketronics_manufacture_cost_report/bt_ketronics_manufacture_cost_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bt_ketronics_manufacture_cost_report.listing', {
#             'root': '/bt_ketronics_manufacture_cost_report/bt_ketronics_manufacture_cost_report',
#             'objects': http.request.env['bt_ketronics_manufacture_cost_report.bt_ketronics_manufacture_cost_report'].search([]),
#         })

#     @http.route('/bt_ketronics_manufacture_cost_report/bt_ketronics_manufacture_cost_report/objects/<model("bt_ketronics_manufacture_cost_report.bt_ketronics_manufacture_cost_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bt_ketronics_manufacture_cost_report.object', {
#             'object': obj
#         })