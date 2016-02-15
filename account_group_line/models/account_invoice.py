# -*- coding: utf-8 -*-
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.tools.translate import _

class account_invoice_makeover(orm.Model):
    _inherit = "account.invoice"

    def group_lines(self, iml, line):
        line = super(account_invoice_makeover,self).group_lines(iml, line)
        if self.journal_id.group_invoice_lines_by_account:
            line2 = {}
            other_lines = []
            for x, y, l in line:
                tmp =   (
                            l['account_id'],
                            l.get('tax_code_id', 'False'),
                            l.get('analytic_account_id', 'False'),
                            l.get('date_maturity', 'False'),
                        )   
                if tmp in line2 and not tmp[2]:
                    am = line2[tmp]['debit'] - line2[tmp]['credit'] + (l['debit'] - l['credit'])
                    line2[tmp]['debit'] = (am > 0) and am or 0.0
                    line2[tmp]['credit'] = (am < 0) and -am or 0.0
                    line2[tmp]['tax_amount'] += l['tax_amount']
                    line2[tmp]['analytic_lines'] += l['analytic_lines']
                    line2[tmp]['product_id'] = False
                    if l['account_id']:
                        line2[tmp]['name'] = self.pool.get('account.account').browse(self._cr, self._uid, l['account_id']).name
                    else:
                        line2[tmp]['name'] = _('Grouping')
                elif tmp not in line2:
                    line2[tmp] = l
                else:
                    other_lines.append(l)
            line = []
            for key, val in line2.items():
                line.append((0,0,val))
            for l in other_lines:
                line.append((0,0,l))
        return line

