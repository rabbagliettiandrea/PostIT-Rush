# Post-It Rush
*La versione attualmente rilasciata è la 0.1 Alpha.*

Il gioco è un racing arcade 2d ed in particolare una competizione tra due o più giocatori
rappresentati mediante un avatar.

## Avatar:
Gli avatar non presentano alcuna differenza tra loro dal punto di vista delle meccaniche di
gioco. La differenziazione dei personaggi è necessaria sia per dare un’affezione al giocatore,
sia per distinguere i personaggi giocanti.
La versione del gioco non presenta la fase di scelta dell’avatar da parte del giocatore,
che è per il momento del tutto casuale.

##Visuale
La visuale è dall’alto, lo scorrimento è verticale: una telecamera osserva il mondo
sottostante da un punto di vista sopraelevato ed è solidale con l’avatar del giocatore, in
quanto lo segue mentre esso avanza sorvolando un mondo cartoon, che presenta in primo
piano tutte le entità con cui l’avatar può interagire.

##Controlli
La particolarità del gioco è il dispositivo di input che il giocatore può scegliere di utilizzare:
la webcam che seguirà i suoi movimenti a destra e a sinistra.

*Nota: La versione 0.1 Alpha presenta un sistema per l’intercettazione dei movimenti del
giocatore più efficiente rispetto a quanto progettato precedentemente. Inizialmente
il dispositivo di input da utilizzare era un post-it (da qui il nome del gioco) applicato
sulla fronte dei giocatori che si sarebbe interfacciato con la macchina tramite la
webcam. Prima di poter giocare, il giocatore si sarebbe dovuto necessariamente
sottoporre ad una breve fase di apprendimento che avrebbe consentito di acquisire
tramite la webcam il colore dell’oggetto, necessario per seguire i movimenti del
giocatore.*


Il giocatore potrà muovere l’avatar influenzandone i movimenti solo sull’asse orizzontale,
dato che l’avatar si muoverà comunque sull’asse verticale, più o meno velocemente, in base
a bonus/malus.
Il giocatore che sceglie di utilizzare come dispositivo di input la webcam per muovere il suo
avatar potrà scegliere se fare in modo che la webcam segua tutti i suoi movimenti (Camera
– Following you) o se utilizzarla con lo stesso comportamento della tastiera (Camera –
Keyboard behavior): inclinadosi verso destra/sinistra, il giocatore spinge l’avatar verso
destra/sinistra finchè non si muoverà fisicamente verso il centro dello schermo, ritornando
nella posizione iniziale. In quest’ultimo caso quindi, lo spostamento destra->sinistra (o
viceversa) dovrà avvenire tramite 3 movimenti ben definiti.
È prevista la possibilità di utilizzare come dispositivo di input alternativo la tastiera e in
questo caso l’avatar si muoverà a destra e a sinistra con i tasti direzionali (destro e sinistro).

##Il gioco
Il gioco non prevede livelli ma il giocatore potrà sceglierne la difficoltà (bassa, media, alta).
Aumentando la difficoltà del gioco, aumenterà il numero degli oggetti del mondo da evitare
(malus/ostacoli), diminuiranno i bonus e aumenterà la velocità di base dell’avatar.
La versione non presenta la fase di scelta della difficoltà del gioco.
Modalità multiplayer
Si implementerà la modalità di multiplayer (su macchine differenti) su TCP/IP ma è
prevista anche una modalità training single player senza avversari per permettere al
giocatore di “allenarsi” prima di sfidare gli amici.
Per la modalità training, il giocatore potrà decidere la lunghezza del mondo in numero di
schermate e la difficoltà (bassa, media, alta). Per ogni corsa di “allenamento” si riporterà il
tempo che l’avatar ha impiegato per raggiungere il traguardo, in modo tale da permettere
al giocatore di battere il suo record più volte prima della sfida.
I giocatori si sfideranno in un ambiente comune e potranno vedersi tra loro. Solo in
caso di netto vantaggio si perderà la visibilità dell’altro.
La versione non implementa la modalità multiplayer e mostra un esempio di corsa di
“allenamento” senza avversari di bassa difficoltà in un mondo di lunghezza predefinita.

##HUD
Durante il gioco (modalità multiplayer) saranno visibili per ogni giocatore poche
informazioni tra cui:

* l’avatar e il nome del giocatore;
* due emoticon che indicano quale giocatore è in vantaggio e quale è in svantaggio;
* gli oggetti intercettati dall’avatar di volta in volta;
* un indicatore per la velocità corrente (espressa con 3 simboli di soglia);

Nella modalità training, invece, sarà visibile oltre all’avatar e al nome del giocatore, anche il
il tempo e il record precedente (se esiste per quella coppia nome-avatar).
Nella versione l’HUD non è presente.

##Menu
Avviato il gioco, il menu principale sarà di questo tipo:

* New game
* Options
* Exit

Selezionando “New game” si avrà:

* Multiplayer
* Training Mode (Single Player)
* Main menu

Una volta selezionato il tipo di modalità di gioco si avrà una schermata per la scelta della
lunghezza del tracciato espressa in numero di schermate, della difficoltà (a cura di chi ospita
la partita), inserimento del nome, scelta dell’avatar e del tipo di dispositivo di input da
utilizzare (camera o keyboard).
Nella versione attuale, ciò che appare all’avvio del gioco è il manuale utente. 
Premendo [spazio] il menu è il seguente:

* Start game (Camera - Keyboard behavior)
* Start game (Camera - Following you)
* Start game (Keyboard)
* Exit