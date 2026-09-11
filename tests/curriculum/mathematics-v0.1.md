# Acceptance tests — Curriculum Matematica v0.1

Questi test verificano la **coerenza pedagogica** del grafo. Non sono ancora test automatici di codice; definiscono il comportamento che il motore dovrà rispettare.

## A. Integrità del grafo

### A1 — Identificatori

- ogni competenza ha un `id` stabile con prefisso `math.`;
- nessun identificatore è riutilizzato per concetti diversi;
- i prerequisiti devono riferirsi a nodi esistenti nel curriculum.

**Atteso:** pass.

### A2 — Nessuna dipendenza circolare intenzionale

Le relazioni di prerequisito devono descrivere una progressione aciclica. Un nodo può essere rivisitato, ma la rivisitazione non deve diventare un prerequisito circolare.

**Atteso:** pass.

### A3 — Copertura dei nuclei

Il curriculum deve coprire lungo il triennio:

- Numeri;
- Geometria / spazio e figure;
- Relazioni e funzioni;
- Dati e probabilità;
- pratiche matematiche trasversali.

**Atteso:** pass.

## B. Gateway e recupero

### B1 — Frazioni prima delle proporzioni

Profilo fittizio:

- classe: 2ª media;
- obiettivo: proporzioni;
- sa applicare meccanicamente il prodotto incrociato;
- fallisce equivalenza e semplificazione di frazioni;
- non sa spiegare il significato di un rapporto.

Percorso atteso:

`math.numbers.proportions`
→ diagnosi prerequisiti
→ `math.numbers.ratios`
→ `math.numbers.fraction-equivalence`
→ recupero mirato
→ nuova verifica
→ ritorno a rapporti
→ ritorno a proporzioni.

**Non accettabile:** continuare con venti proporzioni quasi identiche.

### B2 — Equazioni e segni

Profilo fittizio:

- classe: 3ª media;
- obiettivo: equazioni di primo grado;
- comprende l'idea di uguaglianza;
- commette errori sistematici quando compaiono numeri negativi.

Percorso atteso:

`math.relations.first-degree-equations`
→ `math.relations.algebraic-expressions`
→ diagnosi
→ `math.numbers.signed-operations`
→ recupero specifico
→ verifica sui segni
→ ritorno alle espressioni
→ ritorno alle equazioni.

**Non accettabile:** classificare automaticamente ogni errore come “non sa le equazioni”.

### B3 — Pitagora e radice

Profilo fittizio:

- classe: 2ª media;
- riconosce correttamente il triangolo rettangolo;
- imposta `c² = a² + b²`;
- non comprende come ricavare `c` dal quadrato.

Percorso atteso:

`math.geometry.pythagoras`
→ `math.numbers.square-root`
→ recupero del significato di radice
→ ritorno a Pitagora.

**Non accettabile:** ripetere la classificazione dei triangoli se l'evidenza indica che quella parte è già solida.

### B4 — Area contro perimetro

Profilo fittizio:

- classe: 2ª media;
- conosce formule a memoria;
- in un rettangolo somma i lati quando viene chiesta l'area.

Percorso atteso:

`math.geometry.areas-polygons`
→ `math.geometry.area-concept`
→ attività concettuale su misura bidimensionale
→ confronto area/perimetro
→ ritorno alle aree dei poligoni.

**Non accettabile:** proporre altre formule di aree come prima risposta.

## C. Progressione di difficoltà

### C1 — Difficoltà non equivale a numeri più grandi

Dato un esercizio di frazioni Band 2, una versione Band 3 o Band 4 deve aumentare almeno una dimensione cognitiva rilevante, per esempio:

- scelta della strategia;
- cambio di rappresentazione;
- numero di passaggi concettuali;
- trasferimento a un contesto nuovo;
- necessità di giustificare.

**Non accettabile:** cambiare `3/4` in `137/428` lasciando identico il ragionamento e chiamarlo “livello avanzato”.

### C2 — Anno e difficoltà sono separati

Uno studente di 3ª media può ricevere un'attività Band 1 su un prerequisito di 1ª media durante un recupero, senza che TutorLab lo etichetti come “studente di prima”.

Viceversa uno studente di 1ª media molto solido può ricevere una Band 4 su una competenza di prima, senza anticipare necessariamente il programma di seconda.

**Atteso:** il motore distingue `typical_year`, `challenge_band` e padronanza individuale.

## D. Rappresentazioni

### D1 — Proporzionalità

La padronanza di `math.relations.direct-proportionality` non è confermata da una sola serie di proporzioni numeriche.

Servono evidenze in almeno due rappresentazioni tra:

- situazione verbale;
- tabella;
- rapporto/costante;
- formula;
- grafico.

**Atteso:** la verifica campiona più di una rappresentazione.

### D2 — Dati

Uno studente che sa calcolare la media ma non sa scegliere tra media, mediana e moda non ha ancora piena padronanza di `math.data.central-tendency`.

**Atteso:** consolidare con confronti tra distribuzioni, non soltanto con altre medie aritmetiche.

## E. Problem solving

### E1 — Parole chiave vietate come strategia primaria

Dato un problema, TutorLab non deve insegnare regole del tipo:

- “se trovi ‘in tutto’ devi sommare”;
- “se trovi ‘ognuno’ devi dividere”.

Deve invece far rappresentare quantità e relazione.

**Atteso:** usare `math.practice.problem-representation`.

### E2 — Informazioni irrilevanti

A difficoltà crescente, un problema può contenere dati irrilevanti, ma il carico informativo deve essere intenzionale e coerente con il Difficulty Engine.

**Atteso:** `information_load` cresce esplicitamente; non viene aggiunto rumore casuale.

## F. Fine ciclo

### F1 — Profilo di terza media

Un profilo considerato solido alla fine del ciclo deve avere evidenze distribuite su:

- calcolo e rappresentazioni numeriche;
- geometria piana e solida;
- relazioni e funzioni;
- dati e probabilità;
- problem solving;
- argomentazione;
- trasferimento.

**Non accettabile:** dichiarare una padronanza globale della matematica soltanto da accuratezza procedurale.

## Definition of Done del macro-blocco

Il macro-blocco Curriculum Matematica v0.1 è accettabile quando:

1. i tre anni hanno nodi strutturati;
2. i gateway verticali sono espliciti;
3. ogni nodo significativo ha prerequisiti, obiettivi ed evidenze;
4. il curriculum distingue prescrizione ufficiale e sequenza TutorLab;
5. la transizione normativa 2026/27 è documentata;
6. i percorsi diagnostici sopra descritti sono rappresentabili nel grafo;
7. il curriculum è pronto per essere consumato dal futuro decision engine senza richiedere un indice di libro scolastico.
