# Matematica — scuola secondaria di primo grado

Questo modulo rappresenta il curriculum matematico di TutorLab come **grafo di competenze e prerequisiti**, non come indice lineare di capitoli.

## Principio

La classe scolastica indica il momento tipico in cui una competenza viene affrontata, ma non decide da sola cosa proporre allo studente. TutorLab deve usare tre livelli distinti:

1. **quadro curricolare** — ciò che il sistema scolastico richiede;
2. **sequenza tipica TutorLab** — una progressione didattica ragionevole e versionata;
3. **percorso individuale** — il tragitto effettivo dello studente, determinato da evidenze, prerequisiti e obiettivi.

Per questo `typical_year` non significa «questa competenza può essere insegnata solo in quell'anno».

## Quadro normativo 2026/27

TutorLab deve gestire la transizione normativa italiana senza appiattirla.

- Le nuove Indicazioni nazionali 2025 vengono adottate dall'a.s. 2026/27 a partire dalle classi prime della secondaria di primo grado.
- Le classi seconde e terze già funzionanti nel 2025/26 proseguono con le Indicazioni previgenti fino alla conclusione del rispettivo corso.
- Le Indicazioni nazionali definiscono soprattutto competenze e obiettivi al termine del ciclo; la distribuzione puntuale tra 1ª, 2ª e 3ª media qui proposta è quindi una **sequenza interna TutorLab**, non una prescrizione ministeriale.

Il profilo v0.1 è costruito per essere compatibile con entrambi i quadri durante la transizione e mette al centro i nuclei ricorrenti: numeri, spazio e figure, relazioni e funzioni, dati e probabilità, problem solving, argomentazione, modellizzazione e uso consapevole degli strumenti.

## Struttura del grafo

Ogni nodo possiede:

- un identificatore stabile;
- un nucleo disciplinare;
- un anno tipico;
- una priorità (`gateway`, `core`, `supporting`, `extension`);
- prerequisiti espliciti;
- obiettivi osservabili;
- evidenze di padronanza;
- segnali diagnostici;
- leve con cui aumentare o diminuire la difficoltà.

### Priorità

**Gateway** indica una competenza che apre molte strade successive. Una lacuna qui deve pesare molto nelle decisioni adattive. Esempi: quattro operazioni, divisibilità, equivalenza delle frazioni, proporzionalità, aree, Pitagora, algebra simbolica di base.

**Core** indica una competenza centrale ma meno ramificata.

**Supporting** indica strumenti e rappresentazioni che sostengono più nodi.

**Extension** indica obiettivi utili per potenziamento o consolidamento avanzato, senza essere necessari per ogni passaggio successivo.

## Fili verticali principali

### Numeri

`naturali → operazioni → espressioni → potenze → divisibilità → fattorizzazione → MCD/mcm → frazioni → razionali/decimali → rapporti → proporzioni → percentuali → radici → numeri con segno → calcolo razionale`

### Geometria

`enti geometrici → segmenti/angoli → poligoni → triangoli/quadrilateri → perimetro → area → Pitagora → similitudine → circonferenza/cerchio → solidi → superficie e volume`

### Relazioni e funzioni

`sequenze → relazioni tra grandezze → proporzionalità → piano cartesiano → rappresentazioni multiple → linguaggio simbolico → espressioni letterali → equazioni → funzioni elementari`

### Dati e probabilità

`raccolta dati → tabelle/grafici → frequenze → media/mediana/moda → variabilità → probabilità elementare`

### Pratiche matematiche

Problem solving, stima, modellizzazione, argomentazione, controllo del risultato, scelta degli strumenti e pensiero algoritmico attraversano tutti gli anni. Non sono un capitolo finale.

## Regola adattiva fondamentale

Il grafo non deve costringere lo studente a ripercorrere interi anni scolastici. Se uno studente di 3ª media fallisce un'equazione perché non gestisce le operazioni con numeri con segno, TutorLab sospende l'equazione, recupera il prerequisito preciso e poi ritorna all'equazione.

Allo stesso modo, una competenza già solida può essere attraversata rapidamente attraverso una breve verifica di conferma.

## File

- `year-1.json` — prima media, basi numeriche, frazioni, geometria elementare e prime rappresentazioni di dati;
- `year-2.json` — razionali, rapporti/proporzioni, percentuali, aree, Pitagora, statistica e prime funzioni;
- `year-3.json` — numeri con segno, algebra, equazioni, funzioni, geometria solida e probabilità;
- `cross-year-links.json` — dipendenze verticali e gateway tra anni;
- `map.md` — vista sintetica leggibile dal tutor;
- `sources.md` — fonti curricolari e politica di versionamento;
- `../../../tests/curriculum/mathematics-v0.1.md` — acceptance test pedagogici.

## Validazione strutturale

Dalla root del repository:

```bash
python3 tools/validate_curriculum.py
```

Il validatore usa soltanto la standard library e controlla almeno:

- JSON leggibili;
- ID duplicati;
- prerequisiti inesistenti;
- auto-prerequisiti;
- cicli nel grafo;
- coerenza tra file annuale e `typical_year`;
- nuclei e priorità riconosciuti;
- gateway link verso nodi esistenti;
- presenza di obiettivi ed evidenze di padronanza.

Il validatore non sostituisce la revisione pedagogica: un grafo può essere formalmente valido ma didatticamente sbagliato. Gli acceptance test servono precisamente a coprire questa seconda dimensione.

## Stato

Versione curriculum: **0.1.0**

Questa versione definisce l'ossatura. Le famiglie di esercizi complete e il decision engine useranno questo grafo nei macro-blocchi successivi.
