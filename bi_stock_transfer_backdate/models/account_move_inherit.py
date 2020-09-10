# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from  datetime import datetime
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError,Warning


class AccountingUpdate(models.Model):
	_inherit = 'account.move'

	transfer_date = fields.Datetime(String="Date", compute ='_compute_transfer_date')
	remark = fields.Char(String="Remarks")

	@api.multi
	def _compute_transfer_date(self):
		transfer_move = self.env['stock.move'].search([('picking_id.name','=',self.ref)])
		for tr_move_date in transfer_move:
			if tr_move_date.reference == self.ref:
				self.transfer_date = tr_move_date.transfer_date
	
