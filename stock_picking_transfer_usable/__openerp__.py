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
    'name': 'Usable Picking Transfer',
    'version': '0.1',
    'category': 'Warehouse',
    'description': """

    Questo modulo migliora l'usabilità del wizard di trasferimento manuale dei 
    picking (ordini di consegna) fornendo strumenti di filtraggio e selezione 
    multipla delle righe.

    

    INTRODUZIONE:
    
    Per aziende che gestiscono trasferimenti di magazzino importanti, con decine di 
    righe all'interno di un picking (trasferibile anche parzialmente), si verifica 
    abbastanza frequentemente la necessità di selezionare manualmente le righe del
    picking da trasferire e quali invece riservare per un backorder.
    
    Attualmente, il wizard di trasferimento di un picking carica in automatico 
    tante righe quanti sono i movimenti attualmente trasferibili, con quantità 
    preimpostate. L'utente che volesse rimuovere dal wizard una o più righe, 
    dovrebbe cercare senza alcun ausilio da parte dell'interfaccia utente (dunque
    dovendo scorrere potenzialmente centinaia di righe) la riga desiderata e 
    rimuoverla. Tale situazione diventa insostenibile per l'utente qualora dovesse
    essere ripetuta per decine o addirittura centinaia di righe. 
    
    La problematica legata alla ricerca manuale delle righe si verifica anche nel 
    caso, ancor più frequente, in cui l'utente avesse bisogno di verificare la 
    presenza/assenza di una riga ed eventualmente modificarne la quantità da
    trasferire.
    

    
    UTILIZZO:    
    
    Il presente modulo apporta alcune modifiche al wizard di trasferimento picking.
    
    Le righe del wizard sono state dotate di una check-box di selezione allo scopo 
    di fornire all'utente uno strumento di selezione multipla di tali righe. Inoltre
    vengono introdotti i pulsanti "Seleziona Tutti" ed "Inverti Selezione" che 
    facilitano ulteriormente la selezione delle righe.
    
    Viene introdotto un pulsante "Rimuovi Selezionati" che, quando clickato, 
    elimina in automatico tutte le righe selezionate. 
    
    Il wizard viene inoltre dotato di un campo che permette di selezionare un 
    modello di prodotto. Quando viene selezionato un modello di prodotto, al click
    sul tasto "Filtra" le righe del wizard vengono filtrate in modo da mostrare solo
    quei prodotti afferenti al modello selezionato. 
    
    N.B.: Sebbene il wizard mostri solo le righe filtrate, le altre righe restano 
    nascoste ma presenti e saranno normalmente trasferite al momento della conferma
    del wizard.    
    

    
    CONFIGURAZIONE:
    
    Il modulo non necessita di alcuna configurazione aggiuntiva: una volta 
    installato le sue funzionalità sono già tutte pienamente utilizzabili.

""",
    'author': 'Antonio Esposito',
    'website': 'https://it.linkedin.com/in/antonio-esposito-97668782',
    'license': 'AGPL-3',   
    'depends': ['stock', 'product'],
    'data': [
             'wizard/stock_transfer_details.xml',
             ],

    'demo': [],
    'test': [],
    'installable': True,
    'certificate': '',
}
