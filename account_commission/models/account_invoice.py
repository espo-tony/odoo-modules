# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 ISA s.r.l. (<http://www.isa.it>).
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
from openerp.exceptions import ValidationError

class account_invoice_commission(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        res = super(account_invoice_commission,self).onchange_partner_id(type, partner_id, date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id)
        if res and partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner and partner.salesagent_id:
                if partner.salesagent_id.user_id:
                    user = partner.salesagent_id.user_id.id
                elif partner.salesagent_id.user_ids:
                    user = partner.salesagent_id.user_ids.ids[0]
                if  user: 
                    if 'value' in res:
                        res['value'].update({'user_id':user})
                    else:
                        res['value'] = {'user_id':partner.salesagent_id.user_id.id}
        return res

    @api.cr_uid_ids_context
    def action_cancel(self, cr, uid, ids, context=None):
        res = super(account_invoice_commission, self).action_cancel(cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            commission_obj = self.pool.get('account.commission.line')
            commission_ids = commission_obj.search(cr, uid, [('invoice_src_id','=',invoice.id)], context=context)
            commission_obj.unlink(cr, uid, commission_ids, context=context)
        return res
    
    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.invoice_line:
            return {'warning':{'title': _('Warning!'), 'message': _('This invoice already contains some lines, commission on those lines will not be automatically recomputed!')} }
    
    @api.multi
    def create_commission_line(self):
        for inv in self:
            if inv.user_id and inv.user_id.partner_id:
                for line in inv.invoice_line:
                    if line.commission_perc and line.commission_amount:
                        commission_vals = line.prepare_commission_line()
                        for vals in commission_vals:
                            comm = self.env['account.commission.line'].create(vals)
        return True

class account_invoice_line_commission(models.Model):

    _inherit = 'account.invoice.line'

    commission_perc = fields.Float(string="Commission [%]", digits_compute= dp.get_precision('Account'),)
    commission_amount = fields.Float(compute="_compute_commission_amount", store=True, string="Commission", digits_compute= dp.get_precision('Account'),)    
    
    @api.one
    @api.depends('price_subtotal', 'commission_perc')
    def _compute_commission_amount(self):
        self.commission_amount = self.price_subtotal * self.commission_perc / 100.0

    @api.multi
    def product_id_change(self, product_id, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, company_id=None):    
        res = super(account_invoice_line_commission,self).product_id_change(product_id, uom_id, qty=qty, name=name, type=type, partner_id=partner_id, fposition_id=fposition_id, price_unit=price_unit, currency_id=currency_id, company_id=company_id)
           
        if res and res['value'] and partner_id and product_id and type=='out_invoice' and 'user_id' in self._context and self._context['user_id'] and self.pool.get('res.users').browse(self._cr, self._uid, self._context['user_id'], context=self._context).partner_id.salesagent:
            salesagent_id = self.pool.get('res.users').browse(self._cr, self._uid, self._context['user_id'], context=self._context).partner_id
            comm_perc = 0.0            
            
            if product_id and not self.env['product.product'].browse(product_id).no_commission:
                cmp_id = company_id or self._context.get('company_id',False) or self.env['res.users'].browse(self._uid).company_id.id
                company_obj = self.env['res.company']
                company = company_obj.browse(cmp_id)
                product = self.pool.get('product.product').browse(self._cr, self._uid, product_id, context=self._context)

                if salesagent_id.is_overriding:
                    for comm_line in salesagent_id.custom_commission_line_ids:
                        if not comm_line.partner_id or comm_line.partner_id.id == partner_id:
                            if not comm_line.category_id or comm_line.category_id.id == product.categ_id.id:
                                if not comm_line.template_id or comm_line.template_id.id == product.product_tmpl_id.id:
                                    if not comm_line.product_id or comm_line.product_id.id == product.id:
                                        comm_perc = comm_line.commission_perc
                                        break

                if comm_perc == 0.0:                                
                    if company.commission_priority1:
                        comm_perc = company_obj.get_commission_perc(company.commission_priority1, product, partner_id)
                    if not comm_perc and company.commission_priority2:
                        comm_perc = company_obj.get_commission_perc(company.commission_priority2, product, partner_id)                
                    if not comm_perc and company.commission_priority3:
                        comm_perc = company_obj.get_commission_perc(company.commission_priority3, product, partner_id)                
                    if not comm_perc and company.commission_priority4:   
                        comm_perc = company_obj.get_commission_perc(company.commission_priority4, product, partner_id)     
            res['value']['commission_perc'] = comm_perc           
        return res

    @api.model
    def prepare_commission_line(self):
        res = []
        base_amount = self.get_base_amount()
        commission_amount = base_amount * self.commission_perc / 100.0
        if self.invoice_id.type == 'out_refund':
            commission_amount = -commission_amount
        if commission_amount:
            salesagent = self.invoice_id.user_id.partner_id
            dict1 = {'line_src_id':self.id, 'salesagent_id':salesagent.id, 'commission_mode': salesagent.commission_mode, 'base_untaxed':base_amount, 'amount_commission': commission_amount, 'state':'computed'}
            if salesagent.commission_mode == 'invoiced':
                dict1.update({'state':'matured'})

            if salesagent.salesagent_parent_id and salesagent.salesagent_parent_commission_perc:
                parent_commission_amount = base_amount * salesagent.salesagent_parent_commission_perc / 100.0
                if self.invoice_id.type == 'out_refund':
                    parent_commission_amount = -parent_commission_amount                
                dict2 = {'line_src_id':self.id, 'salesagent_id':salesagent.salesagent_parent_id.id, 'commission_mode': salesagent.salesagent_parent_id.commission_mode, 'base_untaxed':base_amount, 'amount_commission': parent_commission_amount, 'state':'computed'}
                if salesagent.salesagent_parent_id.commission_mode == 'invoiced':
                    dict2.update({'state':'matured'})                
                res.append(dict1)
                res.append(dict2)
            else:
                res.append(dict1)                                
        return res        
    
    @api.model
    def get_base_amount(self):
        return self.price_subtotal               