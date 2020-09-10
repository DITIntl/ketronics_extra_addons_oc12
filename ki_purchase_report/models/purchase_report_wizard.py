from odoo import api, fields, models, _
from pprint import pprint
import calendar
import datetime
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import Warning


class KinsoftPurchaseReportWizard(models.TransientModel):
    _name = 'kinsoft.purchase.report.wizard'
    _description = 'Purchase Report / Laporan Pembelian'

    name = fields.Char(string='Name', default="Purchase Report")
    date_start = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    invoice_ids = fields.Many2many(
        comodel_name='account.invoice',
        relation='account_invoice_purchase_report_rel',
        column1='report_id',
        column2='invoice_id',
        string='Invoices'
    )

    invoice_line_ids = fields.Many2many(
        string="Invoice Lines",
        comodel_name="account.invoice.line",
        relation="account_invoice_line_purchase_report_detail_rel",
        column1="report_id",
        column2="invoice_line_id"
    )
    filter = fields.Selection(string="Filter", selection=[('with_faktur', 'With faktur pajak'), ('without_faktur', 'Without faktur pajak'), ], )

    @api.onchange('date_start', 'date_to')
    def onchange_date(self):
        """
        This onchange method is used to check end date should be greater than
        start date.
        """
        if self.date_start and self.date_to and \
                self.date_start > self.date_to:
            raise Warning(_('End date must be greater than start date'))

    def get_idr_currency(self):
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        return idr_curr

    def get_invoice_rate(self, inv):
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        return inv.currency_id._get_conversion_rate(inv.currency_id, idr_curr, self.env.user.company_id, inv.date_invoice)

    def get_total_price(self, line):
        return line.quantity * self.get_unit_price(line)

    def get_unit_price(self, line):
        unit_price = line.price_unit

        if self.is_usd(line.invoice_id.currency_id.id):
            idr_curr = self.env['res.currency'].search(
                [('name', '=', 'IDR')], limit=1)
            unit_price = line.invoice_id.currency_id._convert(
                unit_price, idr_curr, self.env.user.company_id, line.invoice_id.date_invoice)

        return unit_price

    def is_usd(self, currency_id):
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)

        return currency_id == usd_curr.id

    def get_line_pph(self, line):
        default_pph_tax = self.env.user.company_id.pph_23_id
        pph_line_tax = line.invoice_line_tax_ids.filtered(
            lambda tx: tx.id == default_pph_tax.id)
        return pph_line_tax

    def get_line_ppn(self, line):
        # get default ppn account
        default_purchase_tax = self.env.user.company_id.account_purchase_tax_id
        line_tax = None
        loopnum = 1
        line_tax = line.invoice_line_tax_ids.filtered(
            lambda tx: tx.id == default_purchase_tax)

        return line_tax

    def get_filtered_invoice_ids(self):
        # print('filtering invoice id')

        # get invoice months
        first_month = self.date_start.month
        last_month = self.date_to.month
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)

        filtered_invoice_ids = {}

        # self.invoice_ids.filtered(lambda x : x.date_geinvoice.month >= first_month and x.date_invoice.month <= last_month)

        for x_month in range(first_month, last_month+1, 1):
            all_invoices = self.invoice_ids.filtered(
                lambda inv: inv.date_invoice.month == x_month)

            filtered_invoice_ids[x_month] = {
                'monthname': calendar.month_name[x_month],
                'all_invoices': all_invoices,
                'partner_invoices': {},
                'partner_count': 0,
            }

            partners = filtered_invoice_ids[x_month]['all_invoices'].mapped(
                'partner_id')

            filtered_invoice_ids[x_month]['partner_count'] = len(partners)

            for prn in partners:

                partner_invoices = filtered_invoice_ids[x_month]['all_invoices'].filtered(
                    lambda inv: inv.partner_id.id == prn.id)

                dpp_usd = 0.0
                tax_usd = 0.0
                dpp_idr = 0.0
                tax_idr = 0.0

                # fill sum_untaxed_usd
                # print('Partner : ' + prn.name)
                for inv in partner_invoices:
                    if inv.currency_id.id == usd_curr.id:
                        dpp_usd += inv.amount_untaxed
                        tax_usd += inv.amount_tax
                    else:
                        # convert to USD
                        dpp_usd += inv.currency_id._convert(
                            inv.amount_untaxed, usd_curr, self.env.user.company_id, inv.date_invoice)
                        tax_usd += inv.currency_id._convert(
                            inv.amount_tax, usd_curr, self.env.user.company_id, inv.date_invoice)

                    if inv.currency_id.id == idr_curr.id:
                        dpp_idr += inv.amount_untaxed
                        tax_idr += inv.amount_tax
                    else:
                        dpp_idr = inv.currency_id._convert(
                            inv.amount_untaxed, idr_curr, self.env.user.company_id, inv.date_invoice)
                        tax_idr = inv.currency_id._convert(
                            inv.amount_tax, idr_curr, self.env.user.company_id, inv.date_invoice)

                    # print(str(inv.amount_untaxed))
                    # print(str(inv.amount_tax))

                filtered_invoice_ids[x_month]['partner_invoices'][prn.name] = {
                    'partner_name': prn.name,
                    'invoices': partner_invoices,
                    'dpp_usd': dpp_usd,
                    'tax_usd': tax_usd,
                    'dpp_tax_usd': dpp_usd + tax_usd,
                    'dpp_idr': dpp_idr,
                    'tax_idr': tax_idr,
                    'dpp_tax_idr': dpp_idr + tax_idr,
                }

        # pprint(filtered_invoice_ids)
        return filtered_invoice_ids

    def get_ppn_idr(self, lines):
        ppn_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        default_purchase_tax = 2

        # get line with idr
        idr_lines = lines.filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)

        # print('get ppn idr')
        # print('----------------------------------------------------------------')
        for line in idr_lines:
            for tax in line.invoice_line_tax_ids:
                if tax.id == default_purchase_tax:
                    # print(tax.amount / 100 * line.price_subtotal)
                    ppn_idr += tax.amount / 100 * line.price_subtotal

        # get line with usd
        usd_lines = lines.filtered(
            lambda line: line.invoice_id.currency_id.id == usd_curr.id)
        for line in usd_lines:
            for tax in line.invoice_line_tax_ids:
                if tax.id == default_purchase_tax:
                    tax_line_usd = tax.amount / 100 * line.price_unit * line.quantity
                    tax_line_idr = line.invoice_id.currency_id._convert(
                        tax_line_usd, idr_curr, self.env.user.company_id, line.date_invoice)
                    # print(tax_line_idr)
                    ppn_idr += tax_line_idr
        # print('----------------------------------------------------------------')
        # # get all invoices with idr currency
        # idr_invs = invoices.filtered(
        #     lambda inv: inv.currency_id.id == idr_curr.id)
        # for inv in idr_invs:
        #     for line in inv.invoice_line_ids:
        #         for tax in line.invoice_line_tax_ids:
        #             if tax.id == default_purchase_tax:
        #                 ppn_idr += tax.amount / 100 * line.price_subtotal

        # # get all usd invoices
        # usd_invs = invoices.filtered(
        #     lambda inv: inv.currency_id.id == usd_curr.id)

        # for inv in usd_invs:
        #     for line in inv.invoice_line_ids:
        #         for tax in line.invoice_line_tax_ids:
        #             if tax.id == default_purchase_tax:
        #                 ppn_usd = tax.amount / 100 * line.price_subtotal
        #                 ppn_idr += usd_curr._convert(ppn_usd, idr_curr,
        #                                              self.env.user.company_id, inv.date_invoice)

        return ppn_idr

    def get_ppn_idr_inv(self,  line_by_price):
        lines = line_by_price
        # print(lines)
        ppn_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        default_purchase_tax = 2

        # get line with idr
        idr_lines = lines.mapped('invoice_id').filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)

        for idr_lines2 in idr_lines:
            for line in idr_lines2.invoice_line_ids:
                for tax in line.invoice_line_tax_ids:
                    if tax.id == default_purchase_tax:
                        # print(tax.amount / 100 * line.price_subtotal)
                        ppn_idr += tax.amount / 100 * line.price_subtotal

        # get line with usd
        usd_lines = lines.mapped('invoice_id').filtered(
            lambda line: line.currency_id.id == usd_curr.id)
        for usd_lines2 in usd_lines:
            for line in usd_lines2.invoice_line_ids:
                for tax in line.invoice_line_tax_ids:
                    if tax.id == default_purchase_tax:
                        tax_line_usd = tax.amount / 100 * line.price_unit * line.quantity
                        tax_line_idr = line.invoice_id.currency_id._convert(
                            tax_line_usd, idr_curr, self.env.user.company_id, line.date_invoice)
                        # print(tax_line_idr)
                        ppn_idr += tax_line_idr
        return ppn_idr

    def get_ppn_idr_inv_tax(self,  invoice):
        # print(invoice)
        tax = self.env['account.invoice.tax'].search(
            [('tax_id', '=', 2),('invoice_id', '=', invoice.id)], limit=1)
        # print(tax)
        if tax:
            ppn_idr = tax.amount
        else:
            ppn_idr = 0

        return ppn_idr

    def get_dpp_idr(self, lines):
        invoice_ids = lines.mapped('invoice_id')
        # print(invoice_ids)
        dpp_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)

        # get line with idr
        idr_invoices = lines.mapped('invoice_id').filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)
        dpp_idr += sum(idr_invoices.mapped('amount_untaxed'))

        # get line with usd
        # yang ini hasil beda karena cara perhitungan perkaliannya beda
        # usd_invoices = lines.mapped('invoice_id').filtered(lambda inv : inv.currency_id.id == usd_curr.id)
        # for inv in usd_invoices:
        #     dpp_idr += inv.currency_id._convert(inv.amount_untaxed, idr_curr, self.env.user.company_id, inv.date_invoice)

        # pakai cara yang ini
        usd_lines = lines.filtered(
            lambda line: line.invoice_id.currency_id.id == usd_curr.id)
        for line in usd_lines:
            usd_price_unit = line.invoice_id.currency_id._convert(
                line.price_unit, idr_curr, self.env.user.company_id, line.date_invoice)
            dpp_idr += usd_price_unit * line.quantity

        # # get all invoices with idr currency
        # idr_invs = invoices.filtered(
        #     lambda inv: inv.currency_id.id == idr_curr.id)
        # dpp_idr += sum(idr_invs.mapped('amount_untaxed'))

        # # get all usd invoices
        # usd_invs = invoices.filtered(
        #     lambda inv: inv.currency_id.id == usd_curr.id)
        # for inv in usd_invs:
        #     usd_amount_untaxed = inv.amount_untaxed
        #     idr_amount_untaxed = usd_curr._convert(
        #         usd_amount_untaxed, idr_curr, self.env.user.company_id, inv.date_invoice)
        #     dpp_idr += idr_amount_untaxed

        # print('get dpp idr')
        # print('----------------------------------------------------------------')
        # print(dpp_idr)
        # print('----------------------------------------------------------------')
        return dpp_idr

    def get_dpp_idr_inv(self, invoice_line):
        lines = invoice_line
        # print(lines)
        dpp_idr = 0.0
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)

        # get line with idr
        idr_invoices = lines.mapped('invoice_id').filtered(
            lambda inv: inv.currency_id.id == idr_curr.id)
        dpp_idr += sum(idr_invoices.mapped('amount_untaxed'))

        # pakai cara yang ini
        usd_invoices = lines.mapped('invoice_id').filtered(
            lambda inv: inv.currency_id.id == usd_curr.id)

        usd_lines = self.env['account.invoice.line'].search(
            [('invoice_id', '=', usd_invoices.id)])
        for line in usd_lines:
            usd_price_unit = line.invoice_id.currency_id._convert(
                line.price_unit, idr_curr, self.env.user.company_id, line.date_invoice)
            dpp_idr += usd_price_unit * line.quantity

        return dpp_idr

    def get_month_name(self, date):
        return calendar.month_name[date.month]

    # 4
    def get_report_line(self, lines):
        report_line = []
        invoices_mapped = lines.mapped('invoice_id')
        # print(invoices_mapped)
        invoice_qty_on_lines = len(invoices_mapped)
        usd_curr = self.env['res.currency'].search(
            [('name', '=', 'USD')], limit=1)
        idr_curr = self.env['res.currency'].search(
            [('name', '=', 'IDR')], limit=1)
        default_purchase_tax = self.env.user.company_id.account_sale_tax_id
        default_pph_tax = self.env.user.company_id.pph_23_id

        if invoice_qty_on_lines > 1:
            inv_year = invoices_mapped[0].date_invoice.year
            inv_month = invoices_mapped[0].date_invoice.month
            last_day_of_month = calendar.monthrange(inv_year, inv_month)[1]
            invoice_date = datetime.date(
                inv_year, inv_month, last_day_of_month)
        else:
            invoice_date = invoices_mapped.date_invoice

        currency_rate = invoices_mapped[0].currency_id._get_conversion_rate(
            invoices_mapped[0].currency_id, idr_curr, self.env.user.company_id, invoice_date)

        # print('GET REPORT LINE')
        for prod in lines:
            fak_ppn_idr = self.get_ppn_idr_inv_tax(prod.invoice_id)
            fak_dpp_idr = self.get_dpp_idr_inv(prod)

            fak_dpp_ppn_idr = fak_dpp_idr + fak_ppn_idr

            # calculate dpp usd
            dpp_usd = 0
            ppn_usd = 0
            dpp_ppn_usd = 0
            pph_23 = 0

            if prod.invoice_id.currency_id.id == usd_curr.id:
                dpp_usd = sum(prod.mapped('price_subtotal'))
                for line in prod:
                    ppn_usd += (prod.invoice_line_tax_ids.filtered(
                        lambda tx: tx.id == default_purchase_tax).amount / 100) * (line.price_unit * line.quantity)
                dpp_ppn_usd = dpp_usd + ppn_usd
                harga_idr = prod.invoice_id.currency_id._convert(
                    prod.price_unit, idr_curr, self.env.user.company_id, invoice_date)
            else:
                harga_idr = prod.price_unit

            pph_23 += prod.invoice_line_tax_ids.filtered(
                lambda tx: tx.id == default_pph_tax.id).amount / 100 * harga_idr * prod.quantity

            new_line = {
                'is_usd': self.is_usd(prod.invoice_id.currency_id.id),
                'tanggal': prod.invoice_id.date_invoice,
                'bulan': calendar.month_name[invoice_date.month],
                'nomor_faktur': prod.efaktur_masukan,
                'invoice': prod.invoice_id.number,
                'partner': prod.partner_id.name,
                'product': prod.name,
                # 'product': prod.product_id.name,
                'account': prod.account_id.name,
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
            # print('---------------------')


        return report_line

    # 3
    def get_purchase_report_detail(self):

        filtered_invoice_ids = {}
        line_by_paid = self.invoice_line_ids.sorted(
            key=lambda line: line.date_invoice)

        # pprint(line_by_paid)
        report_line = self.get_report_line(line_by_paid)

        filtered_invoice_ids = {
            # 'invoice_line': line_by_paid,
            'report_line': report_line,
        }

        # pprint(filtered_invoice_ids)

        # raise UserError('Mohon maaf tidak bisa ..')

        return filtered_invoice_ids

    def get_purchase_report_detail_faktur(self):

        filtered_invoice_ids = {}
        efaktur_line = self.invoice_line_ids.sorted(
            key=lambda line: line.date_invoice).mapped('efaktur_masukan')
        efaktur_line = list(dict.fromkeys(efaktur_line))
        # pprint(efaktur_line)

        for fak in efaktur_line:
            line_by_faktur = self.invoice_line_ids.sorted(
                key=lambda line: line.date_invoice).filtered(lambda lin: lin.efaktur_masukan == fak)

            # pprint(line_by_faktur)
            report_line = self.get_report_line(line_by_faktur)

            filtered_invoice_ids[fak] = {
                'faktur': fak,
                'invoice_line': line_by_faktur,
                'report_line': report_line,
            }

        # # get invoice months
        # first_month = self.date_start.month
        # last_month = self.date_to.month
        # usd_curr = self.env['res.currency'].search(
        #     [('name', '=', 'USD')], limit=1)
        # idr_curr = self.env['res.currency'].search(
        #     [('name', '=', 'IDR')], limit=1)

        # filtered_invoice_ids = {}
        # # efakturs = self.invoice_ids.sorted(key=lambda inv : inv.date_invoice).mapped('efaktur_id')
        # efakturs = self.invoice_ids.filtered(lambda inv : inv.efaktur_id)
        # efakturs = efakturs.sorted(key=lambda inv : inv.date_invoice).mapped(lambda x : str(x.prefix_berikat or '') + '.' + str(x.efaktur_id.name or ''))

        # for fak in efakturs:
        #     fak_invoices = self.invoice_ids.filtered(
        #         lambda inv: inv.efaktur_id.id == fak.id).sorted(key=lambda inv : inv.date_invoice)

        #     dpp_idr = self.get_dpp_idr(fak_invoices)
        #     ppn_idr = self.get_ppn_idr(fak_invoices)
        #     dpp_ppn_idr = dpp_idr + ppn_idr

        # filtered_invoice_ids[fak] = {
        #     'faktur': fak.name,
        #     'invoices': fak_invoices,
        #     'dpp_idr': dpp_idr,
        #     'ppn_idr': ppn_idr,
        #     'dpp_ppn_idr': dpp_ppn_idr,
        # }

        # pprint(filtered_invoice_ids)

        # raise UserError('Mohon maaf tidak bisa ..')

        return filtered_invoice_ids

    # 1
    def action_submit(self):
        masa_pajak = int(self.date_to.strftime('%m'))
        tahun_pajak = int(self.date_to.strftime('%Y'))

        if (self.filter == 'with_faktur'):
            all_invoices = self.env['account.invoice'].search(
                ['&', '&', '&',
                 ('type', '=', 'in_invoice'),
                 ('state', 'in', ['open', 'paid']),
                 ('efaktur_masukan', '!=', False),
                 ('masa_pajak', '=', masa_pajak),
                 ('tahun_pajak', '=', tahun_pajak),
                 ], order="date_invoice asc")
        elif (self.filter == 'without_faktur'):
            all_invoices = self.env['account.invoice'].search(
                ['&', '&', '&',
                 ('type', '=', 'in_invoice'),
                 ('state', 'in', ['open', 'paid']),
                 ('date_invoice', '>=', self.date_start),
                 ('date_invoice', '<=', self.date_to),
                 ('efaktur_masukan', '=', False),
                 ], order="date_invoice asc")
        else:
            all_invoices = self.env['account.invoice'].search(
                ['|',
                    '&',('type', '=', 'in_invoice'),
                        ('state', 'in', ['open', 'paid']),
                        ('date_invoice', '>=', self.date_start),
                        ('date_invoice', '<=', self.date_to),
                    '&',('type', '=', 'in_invoice'),
                        ('state', 'in', ['open', 'paid']),
                        ('masa_pajak', '=', masa_pajak),
                        ('tahun_pajak', '=', tahun_pajak),
                 ], order="date_invoice asc")

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
            return self.env.ref('ki_purchase_report.action_report_purchase_excel').report_action(self)
        else:
            return self.env.ref('ki_purchase_report.action_kinsoft_purchase_report_detail').report_action(self)
