# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

import logging
from odoo import models


class ReportPurchaseExcel(models.Model):
    _name = "report.ki_purchase_report.report_purchase_excel"

    _logger = logging.getLogger(__name__)
    try:
        _inherit = 'report.report_xlsx.abstract'
    except ImportError:
        _logger.debug('Cannot find report_xlsx module for version 12')

    def generate_xlsx_report(self, workbook, data, obj):
        doc = obj
        sheet = workbook.add_worksheet()

        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True, 'bg_color': '#bfbfbf', 'valign': 'vcenter'})
        format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format3 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format4 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format5 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format6 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'text_wrap':'true'})
        format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format8 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'num_format': 'yyyy-mm-dd'})

        # set height of row
        sheet.set_row(0, 40)

        # set width of column
        sheet.set_column(0, 16, 20)

        # merge first row
        sheet.merge_range('A1:K1', ("DATA PEMBELIAN "+self.env.user.company_id.name), format1)
        period = str(doc.date_start) + ' - ' + str(doc.date_to)

        sheet.merge_range('A3:B3', "Periode: "+period, format4)
        # sheet.write('C3', ' ', format6)

        sheet.write('A5', "TGL ", format2)
        sheet.write('B5', "NO FAKTUR", format2)
        sheet.write('C5', "SUPPLIER", format2)
        sheet.write('D5', "PRODUCT", format2)
        sheet.write('E5', "KATEGORI", format2)
        sheet.write('F5', "QTY", format2)
        sheet.write('G5', "SAT", format2)
        sheet.write('H5', "HARGA", format2)
        sheet.write('I5', "TOTAL HARGA", format2)
        sheet.write('J5', "DPP", format2)
        sheet.write('K5', "PPN", format2)
        sheet.write('L5', "DPP + PPN", format2)
        row = 4
        col = 0
        inv_paid = doc.get_purchase_report_detail()
        # print(inv_paid)
        sum_dpp_idr = 0
        sum_ppn_idr = 0
        sum_dpp_ppn_idr = 0
        sum_total_idr = 0
        # for fak in inv_paid:
        fak_has_print = 0
        dpp_idr_has_print = 0
        ppn_idr_has_print = 0
        dpp_ppn_idr_has_print = 0
        inv_number = 0
        invdate = 0
        dpp_idr = 0
        ppn_idr = 0
        dpp_ppn_idr = 0
        no_faktur = 0
        partner_name = 0

        for line in inv_paid['report_line']:
            # print(line)
            col = 0
            row += 1

            get_inv_number = line['invoice']
            get_invdate = line['tanggal']
            get_no_faktur = line['nomor_faktur']
            get_partner_name = line['partner']
            harga_idr = 0
            get_dpp_idr = line['dpp_idr']
            get_ppn_idr = line['ppn_idr']
            get_dpp_ppn_idr = line['dpp_ppn_idr']

            if (inv_number != get_inv_number):
                inv_number = get_inv_number
                invdate = get_invdate
                sheet.write(row, col, invdate.strftime('%d/%m/%Y'), format8)

                no_faktur = get_no_faktur
                sheet.write(row, col + 1, no_faktur or '', format6)

                partner_name = get_partner_name
                sheet.write(row, col + 2, partner_name, format6)

            # if (get_no_faktur != no_faktur):
            #     no_faktur = get_no_faktur
            #     sheet.write(row, col + 1, no_faktur or '', format6)
            # if (get_partner_name != partner_name):
            #     partner_name = get_partner_name
            #     sheet.write(row, col + 2, partner_name, format6)

            sheet.write(row, col + 3, line['product'], format6)
            sheet.write(row, col + 4, line['account'], format6)
            sheet.write(row, col + 5, '{0:,.2f}'.format(line['qty']), format7)
            sheet.write(row, col + 6, line['sat'], format7)
            sheet.write(row, col + 7, '{0:,.2f}'.format(line['harga']), format7)
            sheet.write(row, col + 8, '{0:,.2f}'.format(line['total_harga']), format7)
            sum_total_idr = sum_total_idr + line['total_harga']
            if (get_dpp_idr != dpp_idr):
                dpp_idr = get_dpp_idr
                sheet.write(row, col + 9, '{0:,.2f}'.format(dpp_idr), format7)
                sum_dpp_idr += dpp_idr
            if (get_ppn_idr != ppn_idr):
                ppn_idr = get_ppn_idr
                if (ppn_idr > 0):
                    sheet.write(row, col + 10, '{0:,.2f}'.format(ppn_idr), format7)
                    sum_ppn_idr += ppn_idr
            if (get_dpp_ppn_idr != dpp_ppn_idr):
                dpp_ppn_idr = get_dpp_ppn_idr
                sheet.write(row, col + 11, '{0:,.2f}'.format(dpp_ppn_idr), format7)
                sum_dpp_ppn_idr += dpp_ppn_idr
        row += 1
        sheet.write(row, col + 8, '{0:,.2f}'.format(sum_total_idr), format5)
        sheet.write(row, col + 9, '{0:,.2f}'.format(sum_dpp_idr), format5)
        sheet.write(row, col + 10, '{0:,.2f}'.format(sum_ppn_idr), format5)
        sheet.write(row, col + 11, '{0:,.2f}'.format(sum_dpp_ppn_idr), format5)
