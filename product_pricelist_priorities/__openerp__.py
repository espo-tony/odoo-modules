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

{
    'name': 'Product pricelist priorities',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Product Pricelist Priorities
Questo modulo introduce il concetto di priorià nelle versioni di listino.

================================================================================

DESCRIZIONE:
  La gestione di base dei listini, in Odoo, prevede che ad ogni listino (sia 
  esso di vendita o di acquisto) sia associato un numero indefinito di versioni
  (all'interno delle versioni sono poi definite le regole), con l'unico vincolo
  che tra tutte le versioni di un listino ne sia valida sempre e soltanto una 
  (ciò equivale a dire che i periodi di validità delle versioni attive non 
  possono sovrapporsi). 
  Inoltre, al momento del reperimento di un prezzo da listino, il sistema tiene in 
  considerazione le sole regole definite nella versione attualmente attiva.
  Infine, Odoo consente la creazioni di versioni aventi 
  periodo di validità illimitato (non impostando la data di inizio, la data di 
  fine o entrambe).
  
  Evidentemente, qualora un listino abbia una versione di durata illimitata (ed
  è spesso il caso, poiché la versione "di default" è generalmente settata con 
  durata illimitata) risulta impossibile inserire ulteriori versioni. 
  Ciò rende estremamente macchinoso, ad esempio, la creazione di versioni di 
  listino promozionali di durata limitata (bisogna agire, oltre che sulla 
  versione promozionale, anche su quella di default, limitandone temporaneamente
  la validità o rendendolo temporaneamente inattivo; inoltre è necessario 
  prestare particolare attenzione nel ripristinare la versione di default al
  termine della promozione per non incorrere in una situazione in cui il listino
  non abbia alcuna versione attiva in un certo periodo). 
  Inoltre, anche qualora si decidesse di percorrere questa strada, bisognerebbe 
  riprodurre, nella nuova versione, una regola per ognuna delle regole 
  appartenenti alla versione di default. Ciò comporterebbe, oltre che un lavoro 
  immenso per l'operatore, anche un appesantimento generale del DB (tradotto in 
  un degradamento delle prestazioni) ed una insensata duplicazione delle 
  informazioni.
  
  La soluzione trovata a questa problematica sta nel dotare ciascuna versione di
  listino di un valore di priorità e dunque consentire la sovrapposizione 
  temporale di due versioni dello stesso listino purché abbiano differente 
  priorità.
  Inoltre, facendo in modo che il sistema reperisca, per ogni prodotto, sempre
  la prima regola congruente tra tutte le sue versioni attualmente valide, 
  facilita immensamente la creazione di versioni specific-purpose contenenti 
  regole per anche solo una manciata di prodotti.

================================================================================

CONFIGURAZIONE:
  L'ordine di priorità è decrescente: una versione con priorità più alta sarà 
  sempre presa in considerazione prima di una versione con priorità più bassa.
  
  Il range di priorità va da 0 ad un numero positivo virtualmente infinito.
  
  Le versioni già presenti sul sistema all'installazione di questo modulo 
  otterranno automaticamente un livello di priorità 10.
  
  Alla creazione di una nuova versione di listino, è richiesto di inserire
  il suo valore di priorità. Qualora tale valore non venisse impostato, il 
  sistema vi assegnerà automaticamente il valore 10.
  
  E' ora possibile far sovrapporre temporalmente due o più versioni attive,
  purché abbiano livelli di priorità differenti.

================================================================================

UTILIZZO E FUNZIONAMENTO:
  L'utilizzo è del tutto trasparente all'utente, il quale non dovrà fare altro
  che (come già avveniva in precedenza) associare un listino ai propri partner.
  
  Ogniqualvolta il sistema deve reperire il prezzo di un prodotto passando dai
  listini (e ciò avviene, ad esempio, sugli ordini di vendita e di acquisto), 
  cerca, tra tutte le versioni attualmente attive del listino selezionato, tutte
  le regole valide per quel prodotto e prende quella appartenente alla versione
  con priorità più alta. Una volta ricavata la regola, il calcolo del prezzo 
  avviene in maniera del tutto analoga a quanto avveniva in precedenza.
""",
    'author': 'Antonio Esposito',
    'website': 'https://it.linkedin.com/in/antonio-esposito-97668782',
    'license': 'AGPL-3',       
    'depends': [
                'product',
                ],
    'data': [
             'views/pricelist_view.xml',
             ],
    'installable': True,
    'auto_install': False,
    'certificate': '',
}
