# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from datetime import date, timedelta

class partner_product_last_price(models.Model):
    _name = 'partner.product.last.price'
    _description = 'Partner-Product Last Price'
    _order = 'product_name ASC'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True, )
    sale_id = fields.Many2one('sale.order', string="Sale Order",)
    product_id = fields.Many2one('product.product', string="Product", required=True, )  
    product_name =  fields.Char(string="Product Name", related="product_id.name", store=True, )
    last_price = fields.Float(string="Last Price", digits_compute= dp.get_precision('Product Price'),)        


    def run_remove_old_price_history(self, cr, uid, context=None):
        
        company_ids = self.pool.get('res.company').search(cr, uid, [('id','>',0)], context=context)
        
        for company_id in company_ids:
            
            add_days = self.pool.get('res.company').browse(cr,uid,company_id,context=context).keep_last_days
            if add_days == 0:
                continue
            
            today_date = date.today() - timedelta(days=add_days)    
            order_ids = self.pool.get('sale.order').search(cr, uid, [('date_order','<',today_date.strftime('%Y-%m-%d')),('company_id','=',company_id)], context=context)
            history_ids = self.search(cr, uid, [('sale_id','in',order_ids)],context=context)
            self.unlink(cr,uid,history_ids,context=context)

        return True

class res_partner_last_price(models.Model):

    _inherit = 'res.partner'

    product_last_price_ids = fields.One2many('partner.product.last.price', 'partner_id', string="Last Prices")
    