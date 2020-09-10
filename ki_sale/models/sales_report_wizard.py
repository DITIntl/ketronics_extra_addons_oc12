import logging
from odoo import api, fields, models, _
from pprint import pprint
import calendar
import datetime
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)

class ButirSalesReportWizard(models.TransientModel):
    _inherit = 'butir.sales.report.wizard'

    def get_ppn_idr(self, lines):
        ppn_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        default_sales_tax = self.env.user.company_id.account_sale_tax_id

        # get line with idr
        idr_lines = lines.filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)

        # print('get ppn idr')
        # print('----------------------------------------------------------------')
        for line in idr_lines:
            for tax in line.invoice_line_tax_ids:
                if tax.id == default_sales_tax.id:
                    # print(tax.amount / 100 * line.price_subtotal)
                    ppn_idr += tax.amount / 100 * line.price_subtotal

        # get line with usd
        usd_invoices = lines.mapped('invoice_id').filtered(lambda inv: inv.currency_id.id == usd_curr.id)
        for inv in usd_invoices:
            if (inv.partner_id.is_base_statement and inv.efaktur_id.end_date):
                invoice_date = inv.efaktur_id.end_date
            else:
                invoice_date = inv.date_invoice

            ppn_idr += inv.currency_id._convert(inv.amount_tax, idr_curr, self.env.user.company_id,
                                                invoice_date)

        return ppn_idr

    def get_dpp_idr(self, lines):
        dpp_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)

        # get line with idr
        idr_invoices = lines.mapped('invoice_id').filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)
        # print('tes1: {}'.format(idr_invoices))
        dpp_idr += sum(idr_invoices.mapped('amount_untaxed'))

        # get line with usd
        usd_invoices = lines.mapped('invoice_id').filtered(lambda inv : inv.currency_id.id == usd_curr.id)
        # print('tes2: {}'.format(usd_invoices))
        # raise UserError(_("Debug!"))
        for inv in usd_invoices:
            if (inv.partner_id.is_base_statement and inv.efaktur_id.end_date):
                invoice_date = inv.efaktur_id.end_date
            else:
                invoice_date = inv.date_invoice

            dpp_idr += inv.currency_id._convert(inv.amount_untaxed, idr_curr, self.env.user.company_id, invoice_date)

        return dpp_idr

    # 4
    def get_report_line(self, lines):
        _logger.warning('kin-------------------------------')
        pprint(lines)
        report_line = []
        invoices_mapped = lines.mapped('invoice_id')
        invoice_qty_on_lines = len(invoices_mapped)
        _logger.warning('kin-------------------------------'+str(invoice_qty_on_lines))
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        default_sales_tax = self.env.user.company_id.account_sale_tax_id
        default_pph_tax = self.env.user.company_id.pph_23_id
        currency_rate = 0
        fak_dpp_idr = self.get_dpp_idr(lines)
        fak_ppn_idr = self.get_ppn_idr(lines)
        fak_dpp_ppn_idr = fak_dpp_idr + fak_ppn_idr

        if invoice_qty_on_lines > 1:
            if invoices_mapped[0].efaktur_id.end_date:
                invoice_date = invoices_mapped[0].efaktur_id.end_date
            else:
                invoice_date = invoices_mapped[0].date_invoice        
        else:
            invoice_date = invoices_mapped.date_invoice

        # print('invoice date: {}'.format(invoice_date))
        currency_rate = invoices_mapped[0].currency_id._get_conversion_rate(invoices_mapped[0].currency_id, idr_curr,
                                                                            self.env.user.company_id, invoice_date)

        product_on_lines = lines.mapped('product_id')
        # disticnt product lines
        product_on_lines = list(dict.fromkeys(product_on_lines))

        # print('GET REPORT LINE')
        if self.filter == 'without_faktur':
            for prod in lines:
                # calculate dpp usd
                dpp_usd = 0
                ppn_usd = 0
                dpp_ppn_usd = 0
                harga_idr = 0
                pph_23 = 0

                if prod.invoice_id.currency_id.id == usd_curr.id:
                    dpp_usd = sum(prod.mapped('price_subtotal'))
                    ppn_usd += (prod.invoice_line_tax_ids.filtered(
                            lambda tx: tx.id == default_sales_tax.id).amount / 100) * (prod.price_unit * prod.quantity)
                    dpp_ppn_usd = dpp_usd + ppn_usd
                    harga_idr = prod.invoice_id.currency_id._convert(prod.price_unit, idr_curr,
                                                                                    self.env.user.company_id, invoice_date)
                else:
                    harga_idr = prod.price_unit

                pph_23 += prod.invoice_line_tax_ids.filtered(
                        lambda tx: tx.id == default_pph_tax.id).amount / 100 * harga_idr * prod.quantity

                new_line = {
                    'is_usd': self.is_usd(prod.invoice_id.currency_id.id),
                    'tanggal': invoice_date,
                    'bulan': calendar.month_name[invoice_date.month],
                    'nomor_faktur': prod.efaktur_text,
                    'invoice': prod.invoice_id.number,
                    'partner': prod.partner_id.name,
                    'product': prod.product_id.name,
                    'qty': sum(prod.mapped('quantity')),
                    'sat': prod.uom_id.name,
                    'dpp_usd': dpp_usd,
                    'ppn_usd': ppn_usd,
                    'dpp_ppn_usd': dpp_ppn_usd,
                    'pph': pph_23,
                    'kurs': currency_rate,
                    'harga': harga_idr,
                    'total_harga': harga_idr * sum(prod.mapped('quantity')),
                    'dpp_idr': fak_dpp_idr,
                    'ppn_idr': fak_ppn_idr,
                    'dpp_ppn_idr': fak_dpp_ppn_idr,
                }
                report_line.append(new_line)

        if self.filter == 'with_faktur':
            for prod in product_on_lines:
                filtered_line_by_prod = lines.filtered(
                    lambda line: line.product_id.id == prod.id)

                filtered_by_price_unit = filtered_line_by_prod.mapped('price_unit')
                # disticnt by price
                filtered_by_price_unit = list(
                    dict.fromkeys(filtered_by_price_unit))

                for prc in filtered_by_price_unit:
                    line_by_price = filtered_line_by_prod.filtered(
                        lambda line: line.price_unit == prc)

                    # calculate dpp usd
                    dpp_usd = 0
                    ppn_usd = 0
                    dpp_ppn_usd = 0
                    harga_idr = 0
                    pph_23 = 0

                    if line_by_price[0].invoice_id.currency_id.id == usd_curr.id:
                        dpp_usd = sum(line_by_price.mapped('price_subtotal'))
                        for line in line_by_price:
                            ppn_usd += (line.invoice_line_tax_ids.filtered(
                                lambda tx: tx.id == default_sales_tax.id).amount / 100) * (line.price_unit * line.quantity)
                        dpp_ppn_usd = dpp_usd + ppn_usd 
                        harga_idr = line_by_price[0].invoice_id.currency_id._convert(line_by_price[0].price_unit, idr_curr, self.env.user.company_id, invoice_date)
                    else:
                        harga_idr = line_by_price[0].price_unit
                    
                    for line in line_by_price:
                        pph_23 += line.invoice_line_tax_ids.filtered(lambda tx : tx.id == default_pph_tax.id).amount / 100 * harga_idr * line.quantity

                    new_line = {
                        'is_usd' : self.is_usd(filtered_line_by_prod[0].invoice_id.currency_id.id),
                        'tanggal': invoice_date,
                        'bulan': calendar.month_name[invoice_date.month],
                        'nomor_faktur': filtered_line_by_prod[0].efaktur_text,
                        'invoice': filtered_line_by_prod[0].invoice_id.number,
                        'partner': filtered_line_by_prod[0].partner_id.name,
                        'product': filtered_line_by_prod[0].product_id.name,
                        'qty': sum(line_by_price.mapped('quantity')),
                        'sat': filtered_line_by_prod[0].uom_id.name,
                        'dpp_usd': dpp_usd,
                        'ppn_usd': ppn_usd,
                        'dpp_ppn_usd': dpp_ppn_usd,
                        'pph': pph_23,
                        'kurs': currency_rate,
                        'harga': harga_idr,
                        'total_harga': harga_idr * sum(line_by_price.mapped('quantity')),
                        'dpp_idr': fak_dpp_idr,
                        'ppn_idr': fak_ppn_idr,
                        'dpp_ppn_idr': fak_dpp_ppn_idr,
                    }
                    report_line.append(new_line)        

        return report_line

    # 1
    def action_submit(self):
        _logger.warning('submit<-------------------------------')
        if (self.filter == 'with_faktur'):
            _logger.warning('1')
            all_invoices = self.env['account.invoice'].search(
            ['&', '&', '&',
             ('type', '=', 'out_invoice'),
             ('state', 'in', ['open', 'paid']),
             ('efaktur_id.end_date', '>=', self.date_start),
             ('efaktur_id.end_date', '<=', self.date_to),
             ], order="efaktur_id asc")

            all_invoices = all_invoices.filtered(
            'efaktur_id').filtered('prefix_berikat')

        elif (self.filter == 'without_faktur'):
            _logger.warning('2')
            all_invoices = self.env['account.invoice'].search(
            ['&', '&', '&', '&',
             ('type', '=', 'out_invoice'),
             ('state', 'in', ['open', 'paid']),
             ('date_invoice', '>=', self.date_start),
             ('date_invoice', '<=', self.date_to),
             ('efaktur_id', '=', False),
             ('is_berikat', '=', False),
             ], order="date_invoice asc")
             
        # pprint(all_invoices)
        _logger.warning('submit>-------------------------------')
        
        all_invoice_lines = self.env['account.invoice.line'].search(
            [('invoice_id', 'in', all_invoices.ids)])
        all_invoice_lines = all_invoice_lines.sorted(
            key=lambda line: line.date_invoice)

        self.write({
            'invoice_ids': [(6, 0, all_invoices.ids)],
            'invoice_line_ids': [(6, 0, all_invoice_lines.ids)],
        })

        return self.get_report()

    # 2
    def get_report(self):
        if self._context.get('excel_report'):
            return self.env.ref('ki_sale.action_report_sales_excel').report_action(self)
        else:
            return super(ButirSalesReportWizard, self).get_report()
