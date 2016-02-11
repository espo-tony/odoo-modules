# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class stock_move_commission(models.Model):

    _inherit = 'stock.move'

    @api.cr_uid_ids_context    
    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type,
                               context=None):
        res = super(stock_move_commission, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context=context)
        if res and move.procurement_id and move.procurement_id.sale_line_id:
            line = move.procurement_id.sale_line_id
            if res:
                res.update({'commission_perc':line.commission_perc,
                            'commission_amount':line.commission_amount,})
        return res    
        