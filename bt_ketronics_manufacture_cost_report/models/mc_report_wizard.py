from odoo import api, fields, models, _
from pprint import pprint
from datetime import *
from odoo.exceptions import UserError


class MCReportWizard(models.TransientModel):
    _name = 'mc.report.wizard'

    name = fields.Char(string='Name', default="Manufacture Cost Report")
    date_from = fields.Date(string="Date start")
    date_to = fields.Date(string="Date to")
    stock_picking_before_ids = fields.Many2many(
        comodel_name='stock.picking',
        relation='mc_report_wizard_stock_picking_rel',
        column1='wizard_id',
        column2='stock_picking_id',
        string='Stock Picking Before'
    )
    report_config_id = fields.Many2one(
        'mc.report.config', string='Report Config')

    # def _get_report_data(self):
    #     report_config = self.env.ref(
    #         'bt_ketronics_manufacture_cost_report.mc_report_config_default')

    #     # get RAW MATERIAL
    #     # get begining
    #     prods = report_config.raw_material_product_ids
    #     begining_date = self.date_from
    #     begining_datetime = datetime(
    #         begining_date.year, begining_date.month, begining_date.day, 0, 0, 0, 342380)
    #     begining_mat_value = 0

    #     for product in prods:
    #         res = product._compute_quantities_dict(
    #             lot_id=None, owner_id=None, package_id=None, from_date=False, to_date=begining_datetime)
    #         product.qty_available = res[product.id]['qty_available']
    #         product.incoming_qty = res[product.id]['incoming_qty']
    #         product.outgoing_qty = res[product.id]['outgoing_qty']
    #         product.virtual_available = res[product.id]['virtual_available']
    #         if product.qty_available > 0:
    #             product.stock_value = res[product.id]['qty_available'] * \
    #                 product.get_history_price(
    #                     self.env.user.company_id.id, begining_datetime)
    #             begining_mat_value += product.stock_value

    #     # get incoiming
    #     raw_mat_inc = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('picking_id.date_done', '>=', self.date_from),
    #          ('picking_id.date_done', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'incoming'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.raw_material_product_ids.ids)
    #          ])

    #     raw_mat_adj = self.env['stock.move'].search(
    #         ['&', '&', '&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id', '=', False),
    #          ('location_id.usage', '=', 'inventory'),
    #          ('location_dest_id.usage', '=', 'internal'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.raw_material_product_ids.ids)
    #          ])

    #     raw_mat_inc = raw_mat_inc.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)
    #     raw_mat_adj = raw_mat_adj.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_raw_inc = sum(raw_mat_inc) + sum(raw_mat_adj)

    #     # Get consumed material for production
    #     raw_mat_mrp = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'mrp_operation'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.raw_material_product_ids.ids)
    #          ])

    #     raw_mat_mrp = raw_mat_mrp.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_consumed = sum(raw_mat_mrp)

    #     # get outgoing
    #     raw_mat_out = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'outgoing'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.raw_material_product_ids.ids)
    #          ])

    #     raw_mat_out = raw_mat_out.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_raw_return = sum(raw_mat_out)

    #     # get ending
    #     prods = report_config.raw_material_product_ids
    #     ending_date = self.date_to
    #     ending_datetime = datetime(
    #         ending_date.year, ending_date.month, ending_date.day, 0, 0, 0, 342380)
    #     ending_mat_value = 0

    #     for product in prods:
    #         res = product._compute_quantities_dict(
    #             lot_id=None, owner_id=None, package_id=None, from_date=False, to_date=ending_datetime)
    #         product.qty_available = res[product.id]['qty_available']
    #         product.incoming_qty = res[product.id]['incoming_qty']
    #         product.outgoing_qty = res[product.id]['outgoing_qty']
    #         product.virtual_available = res[product.id]['virtual_available']
    #         if product.qty_available > 0:
    #             product.stock_value = res[product.id]['qty_available'] * \
    #                 product.get_history_price(
    #                     self.env.user.company_id.id, ending_datetime)
    #             ending_mat_value += product.stock_value

    #     # ----------------------------------------------------------------------------------------
    #     # get compoenent MATERIAL
    #     # get begining
    #     prods = report_config.component_product_ids
    #     comp_begining_date = self.date_from
    #     comp_begining_datetime = datetime(
    #         comp_begining_date.year, comp_begining_date.month, comp_begining_date.day, 0, 0, 0, 342380)
    #     begining_comp_value = 0

    #     for product in prods:
    #         res = product._compute_quantities_dict(
    #             lot_id=None, owner_id=None, package_id=None, from_date=False, to_date=comp_begining_datetime)
    #         product.qty_available = res[product.id]['qty_available']
    #         product.incoming_qty = res[product.id]['incoming_qty']
    #         product.outgoing_qty = res[product.id]['outgoing_qty']
    #         product.virtual_available = res[product.id]['virtual_available']
    #         if product.qty_available > 0:
    #             product.stock_value = res[product.id]['qty_available'] * \
    #                 product.get_history_price(
    #                     self.env.user.company_id.id, comp_begining_datetime)
    #             begining_comp_value += product.stock_value

    #     # get incoiming
    #     comp_mat_inc = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('picking_id.date_done', '>=', self.date_from),
    #          ('picking_id.date_done', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'incoming'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.component_product_ids.ids)
    #          ])

    #     comp_mat_adj = self.env['stock.move'].search(
    #         ['&', '&', '&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id', '=', False),
    #          ('location_id.usage', '=', 'inventory'),
    #          ('location_dest_id.usage', '=', 'internal'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.component_product_ids.ids)
    #          ])

    #     comp_mat_inc = comp_mat_inc.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)
    #     comp_mat_adj = comp_mat_adj.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_comp_inc = sum(comp_mat_inc) + sum(comp_mat_adj)

    #     # Get consumed material for production
    #     comp_mat_mrp = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'mrp_operation'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.component_product_ids.ids)
    #          ])

    #     comp_mat_mrp = comp_mat_mrp.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_comp_consumed = sum(comp_mat_mrp)

    #     # get outgoing
    #     comp_mat_out = self.env['stock.move'].search(
    #         ['&', '&', '&', '&',
    #          ('date', '>=', self.date_from),
    #          ('date', '<=', self.date_to),
    #          ('picking_type_id.code', '=', 'outgoing'),
    #          ('state', '=', 'done'),
    #          ('product_id', 'in', report_config.component_product_ids.ids)
    #          ])

    #     comp_mat_out = comp_mat_out.mapped(
    #         lambda x: (x.price_unit or x.product_id.standard_price) * x.product_uom_qty)

    #     total_comp_out = sum(comp_mat_out)

    #     # get ending
    #     prods = report_config.component_product_ids
    #     comp_ending_date = self.date_to
    #     comp_ending_datetime = datetime(
    #         comp_ending_date.year, comp_ending_date.month, comp_ending_date.day, 0, 0, 0, 342380)
    #     ending_comp_value = 0

    #     for product in prods:
    #         res = product._compute_quantities_dict(
    #             lot_id=None, owner_id=None, package_id=None, from_date=False, to_date=comp_ending_datetime)
    #         product.qty_available = res[product.id]['qty_available']
    #         product.incoming_qty = res[product.id]['incoming_qty']
    #         product.outgoing_qty = res[product.id]['outgoing_qty']
    #         product.virtual_available = res[product.id]['virtual_available']
    #         if product.qty_available > 0:
    #             product.stock_value = res[product.id]['qty_available'] * \
    #                 product.get_history_price(
    #                     self.env.user.company_id.id, comp_ending_datetime)
    #             ending_comp_value += product.stock_value

    #     # ----------------------------------------------------------------------------------------
    #     # get labor cost
    #     labor_accounts = report_config.labor_cost_account_ids
    #     labor_cost = {}
    #     for acc in labor_accounts:
    #         acc_amls = self.env['account.move.line'].search(
    #             ['&', '&',
    #              ('account_id', '=', acc.id),
    #                 ('date_maturity', '>=', self.date_from),
    #                 ('date_maturity', '<=', self.date_to)
    #              ])
    #         # acc_amls = acc_amls.mapped('debit')
    #         total_amls = abs(sum(acc_amls.mapped('debit')) -
    #                          sum(acc_amls.mapped('credit')))
    #         if(total_amls > 0):
    #             labor_cost[acc] = total_amls

    #     # ----------------------------------------------------------------------------------------
    #     # get production cost
    #     overhead_cost_accounts = report_config.overhead_cost_account_ids
    #     overhead_cost = {}
    #     for acc in overhead_cost_accounts:
    #         acc_amls = self.env['account.move.line'].search(
    #             ['&', '&',
    #              ('account_id', '=', acc.id),
    #                 ('date_maturity', '>=', self.date_from),
    #                 ('date_maturity', '<=', self.date_to)
    #              ])
    #         total_amls = abs(sum(acc_amls.mapped('debit')) -
    #                          sum(acc_amls.mapped('credit')))
    #         if(total_amls > 0):
    #             overhead_cost[acc] = total_amls

    #     report_data = {
    #         'material': {
    #             'begining': begining_mat_value,
    #             'incoming': total_raw_inc,
    #             'outgoing': total_raw_return,
    #             'consumed': total_consumed,
    #             'ending': ending_mat_value,
    #         },
    #         'component': {
    #             'begining': begining_comp_value,
    #             'incoming': total_comp_inc,
    #             'outgoing': total_comp_out,
    #             'consumed': total_comp_consumed,
    #             'ending': ending_comp_value,
    #         },
    #         'labor': labor_cost,
    #         'overhead': overhead_cost
    #     }

    #     return report_data

    def get_report_data(self):
        begining_mat_value = 0
        purch_mat_value = 0
        adjust_mat_value = 0
        total_raw_return = 0
        total_consumed = 0
        ending_mat_value = 0
        ending_comp_value = 0
        total_mat_cost = 0
        labor_cost = 0
        overhead_cost = 0
        begining_wip = 0
        ending_wip = 0
        total_wip = 0
        begining_goods = 0
        ending_goods = 0
        total_goods = 0
        total_production_cost = 0

        payable_type = self.env.ref('account.data_account_type_payable')
        payable_accounts = self.env['account.account'].search(
            [('user_type_id', '=', payable_type.id)])

        report_config = self.env.ref(
            'bt_ketronics_manufacture_cost_report.mc_report_config_default')
        akun_persediaan = report_config.realtime_persediaan_material_account_id
        akun_pembelian = report_config.pembelian_material_account_ids
        stock_input_akun = report_config.stock_input_account_id

        akun_persediaan_wip = report_config.persediaan_barang_dalam_proses_account_id
        akun_persediaan_jadi = report_config.persediaan_barang_jadi_account_id

        stock_journal = report_config.stock_journal_id
        purchase_journal = report_config.purchase_journal_id
        adjustment_journal = report_config.adjustment_journal_id

        # get material value
        begin_mat = self.env['account.move.line'].search(
            [('account_id', '=', akun_persediaan.id), ('date', '<', self.date_from)])
        begin_mat = begin_mat.filtered(lambda x: x.move_id.state == 'posted')
        begining_mat_value = sum(begin_mat.mapped('balance'))

        # get purchased material
        if report_config.property_valuation == 'manual':
            purch_aml = self.env['account.move.line'].search(
                ['&', '&', '&',
                    ('account_id', 'in', akun_pembelian.ids),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                    ('debit', '>', 0)
                ])
            # ('journal_id', '=', purchase_journal.id)
            purch_aml = purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')

            # purch_move = purch_aml.mapped('move_id')
            # purch_move = purch_move.filtered(lambda mv: mv.journal_id.id = purchase_journal.id)
            # purch_move = purch_move.filtered(
            #     lambda mv: payable_type.id in mv.line_ids.mapped('account_id.user_type_id').ids)
            # purch_move = purch_move.filtered(lambda mv: mv.state == 'posted')
            # fix_inc_aml = purch_move.mapped('line_ids')
            # fix_inc_aml = fix_inc_aml.filtered(
            #     lambda ln: ln.account_id.id == akun_pembelian.id)

            purch_mat_value = sum(purch_aml.mapped('debit'))

            # inc_mat = self.env['account.move.line'].search(
            #     ['&', '&', ('account_id', '=', akun_pembelian.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
            # inc_mat = inc_mat.filtered(lambda x: x.move_id.state == 'posted')
            # purch_mat_value = sum(inc_mat.mapped('debit'))
        else:
            # inc_mat = self.env['account.move.line'].search(
            #     ['&', '&', ('account_id', '=', akun_persediaan.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
            # inc_mat = inc_mat.filtered(lambda x: x.move_id.state == 'posted')
            # purch_mat_value = sum(inc_mat.mapped('debit'))

            purch_aml = self.env['account.move.line'].search(
                ['&', '&', '&', 
                ('account_id', '=', akun_persediaan.id), 
                ('date', '>=', self.date_from), 
                ('date', '<=', self.date_to), ('debit', '>', 0),
                ('journal_id', '=', stock_journal.id),
                ])
            purch_aml = purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')
            # purch_move = purch_aml.mapped('move_id')
            # purch_move = purch_move.filtered(
            #     lambda mv: stock_input_akun.id in mv.line_ids.mapped('account_id').ids)
            # purch_move = purch_move.filtered(lambda mv: mv.state == 'posted')
            # fix_purch_aml = purch_move.mapped('line_ids')
            # fix_purch_aml = fix_purch_aml.filtered(
            #     lambda ln: ln.account_id.id == akun_persediaan.id and ln.debit > 0)
            purch_mat_value = sum(purch_aml.mapped('debit'))

        # get adjustment
        if report_config.property_valuation == 'manual':
            adjust_aml = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', 'in', akun_pembelian.ids),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to),
                 ('journal_id', '=', adjustment_journal.id)
                 ])
            adjust_aml = adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
            # adjust_move = adjust_aml.mapped('move_id')
            # for pay_acc in payable_accounts:
            #     adjust_move = adjust_move.filtered(
            #         lambda mv: pay_acc.id not in mv.line_ids.mapped('account_id').ids)
            # adjust_move = adjust_move.filtered(
            #     lambda mv: akun_persediaan_wip.id not in mv.line_ids.mapped('account_id').ids)
            # adjust_move = adjust_move.filtered(lambda mv: mv.state == 'posted')
            # fix_adjust_aml = adjust_move.mapped('line_ids')
            # fix_adjust_aml = fix_adjust_aml.filtered(
                # lambda ln: ln.account_id.id == akun_pembelian.id)
            adjust_mat_value = sum(adjust_aml.mapped('balance'))
        else:
            adjust_aml = self.env['account.move.line'].search(
                ['&', '&', 
                ('account_id', '=', akun_persediaan.id), 
                ('date', '>=', self.date_from), 
                ('date', '<=', self.date_to),
                ('journal_id', '=', adjustment_journal.id)
                ])
            adjust_aml = adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
            # adjust_move = adjust_aml.mapped('move_id')
            # adjust_move = adjust_move.filtered(
            #     lambda mv: stock_input_akun.id not in mv.line_ids.mapped('account_id').ids)
            # adjust_move = adjust_move.filtered(
            #     lambda mv: akun_persediaan_wip.id not in mv.line_ids.mapped('account_id').ids)
            # adjust_move = adjust_move.filtered(lambda mv: mv.state == 'posted')
            # fix_adjust_aml = adjust_move.mapped('line_ids')
            # fix_adjust_aml = fix_adjust_aml.filtered(
            #     lambda ln: ln.account_id.id == akun_persediaan.id)
            adjust_mat_value = sum(adjust_aml.mapped('balance'))
            

        # get retur move
        if report_config.property_valuation == 'manual':
            payable_aml = self.env['account.move.line'].search(
                ['&', '&', '&', ('account_id', 'in', payable_accounts.ids), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('debit', '>', 0)])
            payable_move = payable_aml.mapped('move_id')
            payable_move = payable_move.filtered(
                lambda mv: akun_pembelian.ids in mv.line_ids.mapped('account_id').ids)
            payable_move = payable_move.filtered(
                lambda mv: mv.state == 'posted')
            fix_payable_aml = payable_move.mapped('line_ids')
            fix_payable_aml = fix_payable_aml.filtered(
                lambda ln: ln.account_id.id == akun_pembelian.ids and ln.credit > 0)
            total_raw_return = sum(fix_payable_aml.mapped('credit'))
        else:
            return_aml = self.env['account.move.line'].search(
                ['&', '&', '&', ('account_id', '=', akun_persediaan.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('credit', '>', 0)])
            return_move = return_aml.mapped('move_id')
            return_move = return_move.filtered(
                lambda mv: stock_input_akun.id in mv.line_ids.mapped('account_id').ids)
            return_move = return_move.filtered(lambda mv: mv.state == 'posted')
            fix_return_aml = return_move.mapped('line_ids')
            fix_return_aml = fix_return_aml.filtered(
                lambda ln: ln.account_id.id == akun_persediaan.id and ln.credit > 0)
            total_raw_return = sum(fix_return_aml.mapped('credit'))

        # payable_type = self.env.ref('account.data_account_type_payable')
        # payable_accounts = self.env['account.account'].search(
        #     [('user_type_id', '=', payable_type.id)])
        # payable_aml = self.env['account.move.line'].search(
        #     ['&', '&', '&', ('account_id', 'in', payable_accounts.ids), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('debit', '>', 0)])
        # payable_move = payable_aml.mapped('move_id')
        # payable_move = payable_move.filtered(
        #     lambda mv: akun_persediaan.id in mv.line_ids.mapped('account_id').ids)
        # payable_move = payable_move.filtered(lambda mv: mv.state == 'posted')
        # fix_payable_aml = payable_move.mapped('line_ids')
        # fix_payable_aml = fix_payable_aml.filtered(
        #     lambda ln: ln.account_id.id == akun_persediaan.id and ln.credit > 0)
        # total_raw_return = sum(fix_payable_aml.mapped('credit'))

        ending_mat = self.env['account.move.line'].search(
            [('account_id', '=', akun_persediaan.id), ('date', '<=', self.date_to)])
        ending_mat = ending_mat.filtered(lambda x: x.move_id.state == 'posted')
        ending_mat_value = sum(ending_mat.mapped('balance'))

        total_mat_cost = begining_mat_value + purch_mat_value + \
            adjust_mat_value - total_raw_return - ending_mat_value

        # ----------------------------------------------------------------------------------------
        # get labor cost
        labor_accounts = report_config.labor_cost_account_ids
        labor_cost = {}
        labor_cost_value = 0

        lbr_aml = self.env['account.move.line'].search([
            ('account_id', 'in', labor_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        lbr_aml = lbr_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        labor_cost_value = abs(sum(lbr_aml.mapped('balance')))

        for acc in labor_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            # acc_amls = acc_amls.mapped('debit')
            # total_amls = abs(sum(acc_amls.mapped('debit')) -
            #                  sum(acc_amls.mapped('credit')))
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if(total_amls > 0):
                labor_cost[acc] = total_amls

        # ----------------------------------------------------------------------------------------
        # get production cost
        overhead_cost_accounts = report_config.overhead_cost_account_ids
        overhead_cost = {}
        overhead_cost_value = 0

        ovh_aml = self.env['account.move.line'].search([
            ('account_id', 'in', overhead_cost_accounts.ids),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)
        ])
        ovh_aml = ovh_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        overhead_cost_value = abs(sum(ovh_aml.mapped('balance')))

        for acc in overhead_cost_accounts:
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                 ])
            acc_amls = acc_amls.filtered(
                lambda ac: ac.move_id.state == 'posted')
            # total_amls = abs(sum(acc_amls.mapped('debit')) -
            #                  sum(acc_amls.mapped('credit')))
            total_amls = abs(sum(acc_amls.mapped('balance')))
            if(total_amls > 0):
                overhead_cost[acc] = total_amls

        total_production_cost = total_mat_cost + overhead_cost_value + labor_cost_value

        # ----------------------------------------------------------------------------------------
        # get WIP
        begining_wip_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<', self.date_from)
             ])
        begining_wip_aml = begining_wip_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        begining_wip = sum(begining_wip_aml.mapped('balance'))

        ending_wip_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<=', self.date_to)
             ])
        ending_wip_aml = ending_wip_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        ending_wip = sum(ending_wip_aml.mapped('balance'))
        total_wip = begining_wip + total_production_cost - ending_wip

        # ----------------------------------------------------------------------------------------
        # Get Goods
        begining_goods_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_jadi_account_id.id),
             ('date', '<', self.date_from)
             ])
        begining_goods_aml = begining_goods_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        begining_goods = sum(begining_goods_aml.mapped('balance'))

        ending_goods_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_jadi_account_id.id),
             ('date', '<=', self.date_to)
             ])
        ending_goods_aml = ending_goods_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        ending_goods = sum(ending_goods_aml.mapped('balance'))

        total_goods = begining_goods + total_production_cost - ending_goods

        report_data = {
            'material': {
                'begining': begining_mat_value,
                'purchase': purch_mat_value,
                'adjust': adjust_mat_value,
                'return': total_raw_return,
                'ending': ending_mat_value,
                'total': total_mat_cost,
            },
            'labor': labor_cost,
            'overhead': overhead_cost,
            'total_production_cost': total_production_cost,
            'wip': {
                'begining': begining_wip,
                'ending': ending_wip,
                'total': total_wip,
            },
            'goods': {
                'begining': begining_goods,
                'total_goods': begining_goods + total_wip,
                'ending': ending_goods,
            },
            'cogm': begining_goods + total_wip - ending_goods
        }

        # raise UserError('Mohon maaf tidak bisa ..')
        return report_data

    def action_submit(self):
        # # show current view
        # return {
        #     'name': 'Manufacture Cost Report',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mc.report.wizard',
        #     'type': 'ir.actions.act_window',
        #     'res_id': self.id,
        #     'target': 'current',
        # }

        return self.env.ref('bt_ketronics_manufacture_cost_report.mc_report_action').report_action(self)

        # tree_view_id = self.env.ref('stock_account.view_stock_product_tree2').id
        # form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
        # search_view_id = self.env.ref('stock_account.view_inventory_valuation_search').id
        # # We pass `to_date` in the context so that `qty_available` will be computed across
        # # moves until date.
        # action = {
        #     'type': 'ir.actions.act_window',
        #     'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
        #     'view_mode': 'tree,form',
        #     'name': _('Inventory Valuation'),
        #     'res_model': 'product.product',
        #     'domain': "[('type', '=', 'product'), ('qty_available', '!=', 0)]",
        #     'context': dict(self.env.context, to_date=self.date_from, company_owned=True, create=False, edit=False),
        #     'search_view_id': search_view_id
        # }
        # return action
