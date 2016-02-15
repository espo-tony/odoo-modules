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
from openerp.exceptions import ValidationError

class sale_order_line_last_price(models.Model):

    _inherit = 'sale.order.line'

    def button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order_line_last_price,self).button_confirm(cr, uid, ids, context=context)        
        last_price_obj = self.pool.get('partner.product.last.price')
        
        for line in self.browse(cr,uid,ids,context=context):
            if line.product_id:
                order = line.order_id
                product = line.product_id
                partner = line.order_id.partner_id
                price = line.price_unit * (1 - (line.discount)/100)
                
                last_price_id = last_price_obj.search(cr,uid,[('product_id','=',product.id),('partner_id','=',partner.id)],limit=1,context=context)
                
                if last_price_id:
                    last_price_obj.write(cr, uid, last_price_id, {'sale_id':order.id,'last_price':price})
                else:
                    last_price_obj.create(cr, uid, {'sale_id':order.id,'product_id':product.id,'partner_id':partner.id,'last_price':price})                
            else:
                continue
            
        return res
