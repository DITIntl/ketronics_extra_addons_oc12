# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

import logging
from odoo import models


class ReportSalesExcel(models.Model):
    _name = "report.ki_sale.report_sales_excel"

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
        sheet.merge_range('A1:Q1', ("DATA PENJUALAN "+self.env.user.company_id.name), format1)
        period = str(doc.date_start) + ' - ' + str(doc.date_to)

        sheet.merge_range('A3:B3', "Periode: "+period, format4)
        # sheet.write('C3', ' ', format6)

        sheet.write('A5', "TGL ", format2)
        sheet.write('B5', "BULAN", format2)
        sheet.write('C5', "NO FAKTUR", format2)
        sheet.write('D5', "CUSTOMER", format2)
        sheet.write('E5', "PRODUCT", format2)
        sheet.write('F5', "QTY", format2)
        sheet.write('G5', "SAT", format2)
        sheet.write('H5', "DPP (USD)", format2)
        sheet.write('I5', "PPN (USD)", format2)
        sheet.write('J5', "DPP + PPN (USD)", format2)
        sheet.write('K5', "PPH 23", format2)
        sheet.write('L5', "KURS", format2)
        sheet.write('M5', "HARGA (IDR)", format2)
        sheet.write('N5', "TOTAL HARGA (IDR)", format2)
        sheet.write('O5', "DPP (IDR)", format2)
        sheet.write('P5', "PPN (IDR)", format2)
        sheet.write('Q5', "DPP + PPN (IDR)", format2)
        row = 4
        col = 0
        inv_by_faktur = doc.get_sales_report_detail()
        sum_dpp_usd = 0
        sum_ppn_usd = 0
        sum_dpp_ppn_usd = 0
        sum_dpp_idr = 0
        sum_ppn_idr = 0
        sum_dpp_ppn_idr = 0
        sum_total_idr = 0
        if doc.filter == 'without_faktur':  
            # for fak in inv_by_faktur:
            fak_has_print = 0
            dpp_idr_has_print = 0
            ppn_idr_has_print = 0
            dpp_ppn_idr_has_print = 0
            monthname = 0
            invdate = 0
            dpp_idr = 0
            ppn_idr = 0
            dpp_ppn_idr = 0
            no_faktur = 0
            partner_name = 0

            for line in inv_by_faktur['report_line']:
                col = 0
                row += 1

                get_month_name_str = line['bulan']
                get_invdate = line['tanggal']
                get_no_faktur = line['nomor_faktur']
                get_partner_name = line['partner']
                usd_to_idr_rate = 0
                harga_idr = 0
                get_dpp_idr = line['dpp_idr']
                get_ppn_idr = line['ppn_idr']
                get_dpp_ppn_idr = line['dpp_ppn_idr']

                if (invdate != get_invdate):
                    invdate = get_invdate
                    sheet.write(row, col, invdate.strftime('%d/%m/%Y'), format8)
                if (get_month_name_str != monthname):
                    monthname = get_month_name_str
                    sheet.write(row, col + 1, monthname, format6)
                if (get_no_faktur != no_faktur):
                    no_faktur = get_no_faktur
                    sheet.write(row, col + 2, no_faktur, format6)
                if (get_partner_name != partner_name):
                    partner_name = get_partner_name
                    sheet.write(row, col + 3, partner_name, format6)

                sheet.write(row, col + 4, line['product'], format6)
                sheet.write(row, col + 5, '{0:,.2f}'.format(line['qty']), format7)
                sheet.write(row, col + 6, line['sat'], format7)
                if (line['is_usd']):
                    sheet.write(row, col + 7, '{0:,.2f}'.format(line['dpp_usd']), format7)
                    sum_dpp_usd = sum_dpp_usd + line['dpp_usd']

                    if (line['ppn_usd'] > 0):
                        sheet.write(row, col + 8, '{0:,.2f}'.format(line['ppn_usd']), format7)
                        sum_ppn_usd = sum_ppn_usd + line['ppn_usd']

                    sheet.write(row, col + 9, '{0:,.2f}'.format(line['dpp_ppn_usd']), format7)
                    sum_dpp_ppn_usd = sum_dpp_ppn_usd + line['dpp_ppn_usd']

                if (line['pph'] > 0):
                    sheet.write(row, col + 10, '{0:,.2f}'.format(line['pph']), format7)
                if (line['is_usd']):
                    sheet.write(row, col + 11, '{0:,.2f}'.format(line['kurs']), format7)
                sheet.write(row, col + 12, '{0:,.2f}'.format(line['harga']), format7)
                sheet.write(row, col + 13, '{0:,.2f}'.format(line['total_harga']), format7)
                sum_total_idr = sum_total_idr + line['total_harga']
                if (get_dpp_idr != dpp_idr):
                    dpp_idr = get_dpp_idr
                    sheet.write(row, col + 14, '{0:,.2f}'.format(line['dpp_idr']), format7)
                    sum_dpp_idr += dpp_idr        
            
                if (get_ppn_idr != ppn_idr):
                    ppn_idr = get_ppn_idr
                    if (ppn_idr > 0):
                        sheet.write(row, col + 15, '{0:,.2f}'.format(ppn_idr), format7)
                        sum_ppn_idr += ppn_idr

                if (get_dpp_ppn_idr != dpp_ppn_idr):
                    dpp_ppn_idr = get_dpp_ppn_idr
                    sheet.write(row, col + 16, '{0:,.2f}'.format(dpp_ppn_idr), format7)
                    sum_dpp_ppn_idr += dpp_ppn_idr

        elif doc.filter == 'with_faktur':              
            for fak in inv_by_faktur:
                fak_has_print = 0
                dpp_idr_has_print = 0
                ppn_idr_has_print = 0
                dpp_ppn_idr_has_print = 0
                monthname = 0
                invdate = 0
                dpp_idr = 0
                ppn_idr = 0
                dpp_ppn_idr = 0
                no_faktur = 0
                partner_name = 0

                for line in inv_by_faktur[fak]['report_line']:
                    col = 0
                    row += 1

                    get_month_name_str = line['bulan']
                    get_invdate = line['tanggal']
                    get_no_faktur = line['nomor_faktur']
                    get_partner_name = line['partner']
                    usd_to_idr_rate = 0
                    harga_idr = 0
                    get_dpp_idr = line['dpp_idr']
                    get_ppn_idr = line['ppn_idr']
                    get_dpp_ppn_idr = line['dpp_ppn_idr']

                    if (invdate != get_invdate):
                        invdate = get_invdate
                        sheet.write(row, col, invdate.strftime('%d/%m/%Y'), format8)
                    if (get_month_name_str != monthname):
                        monthname = get_month_name_str
                        sheet.write(row, col + 1, monthname, format6)
                    if (get_no_faktur != no_faktur):
                        no_faktur = get_no_faktur
                        sheet.write(row, col + 2, no_faktur, format6)
                    if (get_partner_name != partner_name):
                        partner_name = get_partner_name
                        sheet.write(row, col + 3, partner_name, format6)

                    sheet.write(row, col + 4, line['product'], format6)
                    sheet.write(row, col + 5, '{0:,.2f}'.format(line['qty']), format7)
                    sheet.write(row, col + 6, line['sat'], format7)
                    if (line['is_usd']):
                        sheet.write(row, col + 7, '{0:,.2f}'.format(line['dpp_usd']), format7)
                        sum_dpp_usd = sum_dpp_usd + line['dpp_usd']

                        if (line['ppn_usd'] > 0):
                            sheet.write(row, col + 8, '{0:,.2f}'.format(line['ppn_usd']), format7)
                            sum_ppn_usd = sum_ppn_usd + line['ppn_usd']

                        sheet.write(row, col + 9, '{0:,.2f}'.format(line['dpp_ppn_usd']), format7)
                        sum_dpp_ppn_usd = sum_dpp_ppn_usd + line['dpp_ppn_usd']

                    if (line['pph'] > 0):
                        sheet.write(row, col + 10, '{0:,.2f}'.format(line['pph']), format7)
                    if (line['is_usd']):
                        sheet.write(row, col + 11, '{0:,.2f}'.format(line['kurs']), format7)
                    sheet.write(row, col + 12, '{0:,.2f}'.format(line['harga']), format7)
                    sheet.write(row, col + 13, '{0:,.2f}'.format(line['total_harga']), format7)
                    sum_total_idr = sum_total_idr + line['total_harga']
                    if (get_dpp_idr != dpp_idr):
                        dpp_idr = get_dpp_idr
                        sheet.write(row, col + 14, '{0:,.2f}'.format(line['dpp_idr']), format7)
                        sum_dpp_idr += dpp_idr        
                
                    if (get_ppn_idr != ppn_idr):
                        ppn_idr = get_ppn_idr
                        if (ppn_idr > 0):
                            sheet.write(row, col + 15, '{0:,.2f}'.format(ppn_idr), format7)
                            sum_ppn_idr += ppn_idr

                    if (get_dpp_ppn_idr != dpp_ppn_idr):
                        dpp_ppn_idr = get_dpp_ppn_idr
                        sheet.write(row, col + 16, '{0:,.2f}'.format(dpp_ppn_idr), format7)
                        sum_dpp_ppn_idr += dpp_ppn_idr

        row += 1
        sheet.write(row, col + 7, '{0:,.2f}'.format(sum_dpp_usd), format5)
        if (sum_ppn_usd > 0):
            sheet.write(row, col + 8, '{0:,.2f}'.format(sum_ppn_usd), format5)
        sheet.write(row, col + 9, '{0:,.2f}'.format(sum_dpp_ppn_usd), format5)
        sheet.write(row, col + 13, '{0:,.2f}'.format(sum_total_idr), format5)
        sheet.write(row, col + 14, '{0:,.2f}'.format(sum_dpp_idr), format5)
        sheet.write(row, col + 15, '{0:,.2f}'.format(sum_ppn_idr), format5)
        sheet.write(row, col + 16, '{0:,.2f}'.format(sum_dpp_ppn_idr), format5)
