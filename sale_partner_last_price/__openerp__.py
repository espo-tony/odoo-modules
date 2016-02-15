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

{
    "name": "Sale Partner Last Price",
    "version": "1.0",
    "category": "Sales Management",
    
    'description': """    
    
    Questo modulo consente di reperire, in maniera semplice e veloce, l'ultimo 
    prezzo applicato ad un cliente relativamente ad un prodotto.

    ================================================================================        

    INTRODUZIONE:
    
    Si verifica sovente l'eventualità in cui un'azienda, pur disponendo di uno o più 
    listini di vendita, applica ad un cliente dei prezzi differenti dai soliti.
    Come conseguenza di tali eventualità, l'azienda (nelle persone dei suoi 
    venditori) potrebbe avere la necessità di reperire qual è stato l'ultimo prezzo
    applicato, relativamente ad un dato prodotto, ad uno specifico cliente.
    
    Allo stato attuale, su Odoo, tale operazione di reperimento comporta la ricerca
    dell'ultimo ordine di vendita intestato al cliente, dunque la ricerca al suo 
    interno della riga di vendita relativa al prodotto d'interesse e del prezzo
    applicatovi; qualora l'ultimo ordine non contenesse il prodotto d'interesse, 
    si rivelerebbe necessario reiterare l'operazione sull'ordine appena precedente e
    così via fino ad ottenere l'informazione desiderata.
    
    ================================================================================
 
    UTILIZZO:    
    
    Il presente modulo introduce nella schermata dei partner clienti la tab "Ultimi
    prezzi di vendita" in cui sono elencati, in ordine alfabetico di prodotto,
    tutti i prodotti venduti almeno in un'occasione al cliente in questione, col 
    riferimento all'ultimo ordine di vendita in cui il prodotto è stato venduto ed 
    il relativo prezzo di vendita (già eventualmente scontato).
    
    ================================================================================
 
    CONFIGURAZIONE:
    
    Il modulo non necessita di alcuna configurazione aggiuntiva: una volta 
    installato le sue funzionalità sono già tutte pienamente utilizzabili.
    
    Poiché la memorizzazione dei prezzi di vendita inizia dal momento in cui il 
    modulo viene installato, prezzi di vendita relativi ad ordini precedenti, pur 
    presenti nel sistema, non saranno comunque visualizzabili attraverso le 
    funzionalità introdotte da questo modulo.

    ================================================================================    

    N.B.:
    
    Alcune aziende potrebbero trovare utile l'opzione di rimuovere automaticamente 
    dal sistema le informazioni relative ai prezzi di vendita applicati così tanto
    tempo addietro da non costituire più informazioni commercialmente utili. E' il 
    caso, ad esempio, di aziende la cui offerta si rinnova periodicamente (come nel 
    caso di aziende operanti nel settore dell'abbigliamento) o il cui prezzario ha 
    un'altissima variabilità (come nel caso di aziende operanti nel settore della
    tecnologia). 
    
    Il presente modulo offre nativamente tale funzionalità, sebbene sia disabilitata
    di default. Per abilitarla è sufficiente andare nel menù 'Configurazione' -> 
    'Technical' -> 'Automation' -> 'Azioni Programmate' e selezionare l'azione 
    'Remove Old Price History'. Nei dettagli di tale azione, flaggare la casella 
    'Attivo' ed impostare, nel campo 'Prossima Data di Esecuzione', la data e l'ora
    in cui si desidera che il sistema esegua automaticamente l'operazione (tenere
    presente che di default tale azione sarà reiterata quotidianamente dal sistema;
    se si desidera modificare la cadenza con cui il sistema esegue l'azione, agire
    sui parametri 'Numero di Intervallo' ed 'Unità di Intervallo').
    Nell'eseguire tale configurazione, in ambienti multi-azienda, ricordare che 
    l'operazione sarà attivata per tutte le aziende.
    
    L'azione rimuoverà dal sistema quei prezzi relativi agli ordini di vendita la 
    cui data d'ordine è inferiore di X giorni (di default 30) dalla data attuale. 
    Per modificare questo parametro, andare nel menù 'Configurazione' -> 'Aziende' 
    -> 'Aziende', selezionare l'azienda per cui si vuole modificare tale parametro e
    dunque modificare il campo 'Rimuovi prezzi vecchi di (giorni)", tenendo presente
    che settare tale campo a '0' significa disattivare l'azione per l'azienda
    corrente.
    
    In pratica, è possibile in un ambiente multi-azienda attivare l'azione di 
    rimozione automatica solo per alcune aziende, attivando l'azione ed impostando
    il campo 'Rimuovi prezzi vecchi di (giorni)' a 0 per quelle aziende a cui si 
    desidera non applicare l'azione.
    
    """,
    
    "license": "AGPL-3",
    'category': 'Sales Management',
    'author': 'Antonio Esposito',
    'website': 'https://it.linkedin.com/in/antonio-esposito-97668782',
    "depends": ["sale",],
    "data": [
             "security/ir.model.access.csv",
             "views/res_partner_view.xml",
             "views/res_company_view.xml",
             "data/remove_old_entries.xml",
             ],
    "installable": True,
}
