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

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp

class sale_order_discount(orm.Model):
    _name = 'sale.order.discount'
    _description = 'Sconto Globale'
    _order = 'sequence ASC'    
    _columns= {
                'name': fields.many2one('account.discount.type', string='Nome', required = True),
                'application': fields.selection([('partner','Cliente'),('payment','Termine di Pagamento'),('general','Generale')], string='Applicazione', required=True),
                'type': fields.selection([('perc','%'),('fisso','Fisso')], string='Tipo', required=True),
                'sequence': fields.integer('Sequence'),
                'value': fields.float('Valore'),
                'sale_id': fields.many2one('sale.order', string='Ordine'),
    }    
    _defaults={
               'sequence': 0,
               'type': 'perc',
               'application': 'general',
    }
    
    def onchange_discount_name(self, cr, uid, ids, name, type, context=None):
        value = {}
        if name:
            disc_obj = self.pool.get('account.discount.type').browse(cr,uid,name)
            if not type:
                value['type'] = disc_obj.type
        return {'value':value}

class sale_order_line(orm.Model):

    _inherit = "sale.order.line"

    _columns = {
        'free': fields.selection([
            ('gift', 'Gift on Amount Total'),
            ('base_gift', 'Gift on Amount Untaxed')],
            'Free')
    }

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False,
                                         context=None):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = {}
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id, context)
        res.update({
            'free': line.free,
        })
        return res

class sale_order_with_discount(orm.Model):

    _inherit = 'sale.order'

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()


    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        return super(sale_order_with_discount,self)._amount_all_wrapper(cr, uid, ids, field_name, arg, context=context)

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):      
        
        res = super(sale_order_with_discount,self)._amount_all(cr,uid,ids,field_name,arg,context=context)        
        cur_obj = self.pool.get('res.currency')

        for order in self.browse(cr, uid, ids, context=context):
                     
            cur = order.pricelist_id.currency_id
            res[order.id]['displayed_global_discount_total'] = 0.0
            res[order.id]['global_discount_total'] = 0.0   
            res[order.id]['amount_untaxed_free'] = 0.0
            res[order.id]['amount_tax_free'] = 0.0            
            
            original_total_value = 0.0
            tax_lines = {}  
                        
            for line in order.order_line:
                if line.free not in ['gift', 'base_gift'] and (not line.product_id or (line.product_id and not line.product_id.no_discount)):  
                    
                    original_tax_value = 0.0
                    for tax in line.tax_id:
                        original_tax_value += line.price_subtotal * tax.amount                       
                    original_untaxed_value = line.price_subtotal
                    original_total_value = original_untaxed_value + original_tax_value
                                
                    for discount in order.global_discount_lines:
        
                       val = original_tax_value
                       val1 = original_untaxed_value
                       val2 = original_total_value
                                        
                       if discount.type=='fisso':
                            res[order.id]['global_discount_total'] += discount.value
                            res[order.id]['displayed_global_discount_total'] += discount.value
                            perc = discount.value / val1                
                       else:
                            perc = discount.value/100
        
                       sc = val*perc 
                       val -= sc
                       sc1 = val1*perc
                       val1 -= sc1
                                          
                       if discount.type=='perc':
                           res[order.id]['global_discount_total']+= sc+sc1
                           res[order.id]['displayed_global_discount_total'] += sc1
                            
                       original_tax_value = cur_obj.round(cr, uid, cur, val)
                       original_untaxed_value = cur_obj.round(cr, uid, cur, val1)
                       original_total_value = original_tax_value + original_untaxed_value
               
                if line.free in ['gift', 'base_gift']:
                    res[order.id]['amount_untaxed_free'] += line.price_subtotal
                    if line.free == 'gift':
                        for tax in line.tax_id:
                            if tax.amount in tax_lines:
                                tax_lines[tax.amount] += line.price_subtotal
                            else:
                                tax_lines[tax.amount] = line.price_subtotal

            for tl in tax_lines:
                res[order.id]['amount_tax_free'] += tax_lines[tl] * tl
                
            res[order.id]['amount_untaxed'] = res[order.id]['amount_untaxed'] - res[order.id]['amount_untaxed_free'] - res[order.id]['displayed_global_discount_total']
            res[order.id]['amount_tax'] = res[order.id]['amount_tax'] - res[order.id]['amount_tax_free'] - (res[order.id]['global_discount_total']-res[order.id]['displayed_global_discount_total'])
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax'] - res[order.id]['global_discount_total']
               
            if original_total_value:   
                res[order.id]['global_discount_percentual'] = res[order.id]['displayed_global_discount_total']/(res[order.id]['amount_untaxed'] + res[order.id]['displayed_global_discount_total'])
            else:
                res[order.id]['global_discount_percentual'] = 0.0
            
        return res



    _columns = {

        'global_discount_lines': fields.one2many('sale.order.discount', 'sale_id', string='Sconti Globali'),                
        'amount_untaxed_free' : fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), multi='sums', string='"For Free" Amount', 
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),                                    
        'amount_tax_free' : fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='"For Free" Tax', multi='sums',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),                                 
        'displayed_global_discount_total' : fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Totale Sconti', multi='sums', help="The amount without tax.", track_visibility='always',
            store={
                   'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                   'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),
        'global_discount_percentual': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Percentuale Sconti', multi='sums', help="The amount without tax.", track_visibility='always',
            store={
                   'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                   'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),                
        'global_discount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Totale Sconti', multi='sums', help="The amount without tax.", track_visibility='always',
            store={
                   'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                   'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),
        'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Untaxed Amount', multi='sums', help="The amount without tax.", track_visibility='always',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),
        'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Taxes', multi='sums', help="The tax amount.", 
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),
        'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total', multi='sums', help="The total amount.",
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','global_discount_lines'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            }),                
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):

        res = super(sale_order_with_discount,self)._prepare_invoice(cr, uid, order=order, lines=lines, context=context)
        if res and order.global_discount_lines:
            discount_lines = []
            for line in order.global_discount_lines:
                discount_lines.append(self.pool.get('account.invoice.discount').create(cr,uid,{'name':line.name.id,'application':line.application, 'type':line.type,'sequence':line.sequence,'value':line.value}))            
            res['global_discount_lines'] = [(6, 0, discount_lines)]
        return res
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order_with_discount, self).onchange_partner_id(cr, uid, ids, part, context = context)
        if part:
            to_delete = []
            discount_lines = []
            sequence = 0    
            part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
            if context.get('discount_lines', False):
                discount_lines = context.get('discount_lines', False)                
                for i in range(len(discount_lines)):
                    if isinstance(discount_lines[i], list):
                        if discount_lines[i][0] == 0:
                            if discount_lines[i][2].get('application',False) == 'partner':
                                to_delete.append(i)
                            elif discount_lines[i][2].get('sequence',False) and discount_lines[i][2].get('sequence') > sequence:
                                sequence = discount_lines[i][2].get('sequence')
                                
                        elif discount_lines[i][0] == 4:
                            discount = self.pool.get('sale.order.discount').browse(cr,uid,discount_lines[i][1])
                            if discount.application == 'partner':
                                to_delete.append(i)
                            elif discount.sequence > sequence:
                                sequence = discount.sequence          
                                            
                    elif isinstance(discount_lines[i], dict):
                        if discount_lines[i].get('application',False) == 'partner':
                            to_delete.append(i)
                        elif discount_lines[i].get('sequence',False) and discount_lines[i].get('sequence') > sequence:
                            sequence = discount_lines[i].get('sequence')

            to_delete = to_delete[::-1]
            for i in to_delete:
                del discount_lines[i]
                        
            for line in part.global_discount_lines:
                discount_lines.append({'name':line.name.id,'type':line.type,'value':line.value, 'application':line.application, 'sequence': sequence+1})
            res['value'].update({'global_discount_lines':discount_lines})         
        return res
    
    def onchange_payment_term(self, cr, uid, ids, payment, context=None):
        res = {}
        if payment:
            discount_lines = []
            to_delete = []            
            sequence = 0            
            payment = self.pool.get('account.payment.term').browse(cr, uid, payment, context=context)
            if context.get('discount_lines', False):
                discount_lines = context.get('discount_lines', False)                
                for i in range(len(discount_lines)):
                    if isinstance(discount_lines[i], list):
                        if discount_lines[i][0] == 0:
                            if discount_lines[i][2].get('application',False) == 'payment':
                                to_delete.append(i)
                            elif discount_lines[i][2].get('sequence',False) and discount_lines[i][2].get('sequence') > sequence:
                                sequence = discount_lines[i][2].get('sequence')
                                
                        elif discount_lines[i][0] == 4:
                            discount = self.pool.get('sale.order.discount').browse(cr,uid,discount_lines[i][1])
                            if discount.application == 'payment':
                                to_delete.append(i)
                            elif discount.sequence > sequence:
                                sequence = discount.sequence          
                                            
                    elif isinstance(discount_lines[i], dict):
                        if discount_lines[i].get('application',False) == 'payment':
                            to_delete.append(i)
                        elif discount_lines[i].get('sequence',False) and discount_lines[i].get('sequence') > sequence:
                            sequence = discount_lines[i].get('sequence')
            elif context.get('partner', False):
                part = self.pool.get('res.partner').browse(cr, uid, context['partner'], context=context)                
                for line in part.global_discount_lines:
                    discount_lines.append({'name':line.name.id,'type':line.type,'value':line.value, 'application':line.application, 'sequence': sequence+1})


            to_delete = to_delete[::-1]
            for i in to_delete:
                del discount_lines[i]
                        
            for line in payment.global_discount_lines:
                discount_lines.append({'name':line.name.id,'type':line.type,'value':line.value, 'application':line.application, 'sequence': sequence+1})
            res = {'value': {'global_discount_lines':discount_lines}}         
        return res    