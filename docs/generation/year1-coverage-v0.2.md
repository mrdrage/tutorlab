# Generation Coverage v0.2 — 1ª media

Questo macro-blocco porta la generation coverage di TutorLab dai due vertical slice iniziali all'intero curriculum di 1ª media per Matematica e Inglese.

## Copertura verificata

La CI legge direttamente i due file curricolari `year-1.json` e richiede che ogni nodo sia presente nella registry generativa.

Copertura corrente verificata:

- Matematica: 20 nodi eseguibili;
- Inglese: 28 nodi eseguibili;
- Totale: 48 nodi eseguibili.

Per ogni nodo la CI costruisce almeno una sessione `advance` e una `reassess` e applica il quality gate del Session Engine.

## Architettura

La copertura è organizzata per famiglie disciplinari, non con un file o una classe per ogni esercizio.

Matematica:

- pratiche matematiche;
- numeri e calcolo;
- frazioni;
- geometria;
- dati e rappresentazioni.

Inglese:

- grammatica di base e grammatica in uso;
- lessico;
- fonologia;
- reading;
- listening;
- spoken interaction;
- spoken production;
- writing;
- mediation;
- learning strategies;
- intercultural awareness.

Le famiglie specializzate già esistenti per `math.numbers.fraction-equivalence` e `eng.grammar.present_simple` restano attive.

## Tipi di task

I task chiusi hanno una soluzione determinabile. I task aperti, inclusi writing, speaking, interaction e mediation, espongono una rubrica lato tutor e richiedono scoring esterno invece di produrre automaticamente una valutazione non giustificata.

Per il listening v0.2 non viene generato audio: il task contiene uno script lato tutor, nascosto dalla student view, che può essere letto dal tutor o trasformato in audio da una futura integrazione.

## Fingerprint v0.2

Il fingerprint include la fase pedagogica oltre a family e parametri. Questo evita che diagnosi, pratica, transfer e verifica vengano considerati duplicati quando condividono gli stessi dati di base, mantenendo comunque l'anti-ripetizione all'interno della stessa funzione didattica.

## Vincolo di regressione

Se in futuro viene aggiunto un nuovo nodo ai curriculum di 1ª media senza una task family generativa, `Year-1 generation coverage` deve fallire. La generation coverage non è quindi una dichiarazione manuale, ma una proprietà verificata del repository.

## Limiti intenzionali

- la coverage completa riguarda per ora soltanto la 1ª media;
- 2ª e 3ª media restano nel curriculum ma possono restituire `needs_review` finché non vengono coperte;
- la qualità disciplinare continuerà a essere raffinata attraverso rubriche, varietà dei task e uso reale con sessioni fittizie/controllate;
- TutorLab genera contenuti originali e non replica esercizi di manuali scolastici.
