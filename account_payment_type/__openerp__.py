# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
{
    'name': "Account Payment Type",
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Account Payment Type
Questo modulo introduce, alle righe di termine di pagamento, un tipo di
pagamento (a scelta tra Contante, Bonifico e Ricevuta Bancaria).
""",
    'author': 'Antonio Esposito',
    'website': 'https://it.linkedin.com/in/antonio-esposito-97668782',
    'license': 'AGPL-3',
    "depends" : ['account',],
    "data" : [
              'views/account_payment_term_line_view.xml',
             ],
    "demo" : [],
    "installable": True
}
