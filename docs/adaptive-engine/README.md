# Adaptive Engine v0.1

TutorLab deve sapere **cosa fare dopo** sulla base di evidenze, prerequisiti e obiettivi. L'Adaptive Engine trasforma osservazioni didattiche in una decisione motivata senza confondere il risultato di un esercizio con una diagnosi.

## Separazione fondamentale

Il motore mantiene distinti tre livelli:

1. **osservazione** — ciò che è accaduto: risposta, tempo, aiuto richiesto, spiegazione, correzione dopo feedback;
2. **inferenza** — ipotesi probabilistica su competenza ed errore;
3. **decisione** — `recover`, `consolidate`, `advance`, `extend` o `reassess`.

Un singolo errore non autorizza una diagnosi forte. Una decisione deve indicare quali evidenze la sostengono e quale incertezza rimane.

## Input logici

L'engine usa:

- `target_competency_id` — obiettivo corrente;
- grafo curricolare della materia;
- eventi di evidenza recenti e storici;
- stato sintetico delle competenze rilevanti;
- Difficulty Engine, quando è disponibile il profilo del task;
- policy adattiva versionata;
- eventuale override del tutor.

Non usa il voto scolastico come sostituto del profilo di competenza.

## Evidence-first

Gli eventi di evidenza sono immutabili. Lo stato dello studente è una **proiezione ricalcolabile** degli eventi, non la fonte primaria.

Ogni evidenza può informare dimensioni diverse:

- accuratezza;
- autonomia;
- stabilità;
- trasferimento;
- spiegazione/ragionamento;
- fluidità o tempo ragionevole;
- comprensione della consegna;
- uso comunicativo, per le lingue.

Il motore deve poter dire: «non ho abbastanza evidenze».

## Mastery profile, non voto unico

Ogni competenza possiede un profilo multidimensionale. Un valore aggregato può servire al routing, ma non sostituisce le dimensioni sottostanti.

Esempio:

```text
accuracy      0.86
independence  0.42
stability     0.71
transfer      0.35
explanation   0.63
fluency       0.58
confidence    0.76
```

Questo profilo descrive uno studente generalmente corretto ma ancora dipendente dalla guida e poco stabile nel trasferimento. La decisione plausibile è `consolidate`, non `advance` automatico.

## Error hypotheses

La tassonomia pedagogica viene trattata come insieme di **ipotesi concorrenti**:

- `conceptual_error`
- `missing_prerequisite`
- `procedure_error`
- `execution_error`
- `instruction_comprehension`
- `strategy_selection`
- `attention_lapse`
- `not_automated`
- `persistent_difficulty`

Ogni ipotesi contiene:

- confidenza;
- evidenze a favore;
- evidenze contrarie;
- competenza collegata, se applicabile;
- persistenza nel tempo.

L'engine non deve diagnosticare condizioni cliniche o disturbi dell'apprendimento.

## Objective stack e ritorno obbligatorio

Quando viene attivato un recupero, TutorLab mantiene uno **stack degli obiettivi**.

Esempio:

```text
TARGET: math.numbers.proportions
  -> RECOVER: math.numbers.ratios
      -> RECOVER: math.numbers.fraction-equivalence
```

Il percorso di recupero non sostituisce l'obiettivo iniziale. Dopo una nuova evidenza sufficiente sul prerequisito, il motore deve risalire lo stack e riprendere l'obiettivo sospeso.

Per evitare deviazioni infinite, la policy definisce un limite di profondità. Se servirebbe scendere ancora, la decisione diventa `reassess` e il tutor riceve una spiegazione.

## Decisioni

### recover

Usata quando una lacuna specifica, spesso in un prerequisito, spiega plausibilmente il fallimento sull'obiettivo corrente.

Deve indicare:

- nodo da recuperare;
- perché quel nodo è causalmente rilevante;
- condizione per tornare all'obiettivo sospeso.

### consolidate

Usata quando l'obiettivo è compreso ma non ancora stabile, autonomo o trasferibile.

Non significa ripetere esercizi identici: il Difficulty Engine deve variare rappresentazione, contesto, strategia o supporto.

### advance

Usata quando le evidenze sono sufficienti e distribuite. Non richiede perfezione, ma nessuna lacuna critica ad alta confidenza deve compromettere i nodi successivi.

### extend

Usata per potenziamento quando la competenza è stabile, autonoma e trasferibile. Non anticipa contenuti fuori programma come scorciatoia; può aumentare apertura, ragionamento, integrazione e autenticità del task.

### reassess

Usata quando le evidenze sono poche, contraddittorie o ambigue. È una decisione valida, non un fallimento del motore.

## Hysteresis didattica

TutorLab evita oscillazioni nervose.

- un singolo errore occasionale non fa retrocedere una competenza stabile;
- una singola risposta corretta non rende padroneggiata una competenza fragile;
- le evidenze recenti pesano di più, ma non cancellano automaticamente uno storico coerente;
- il trasferimento e l'autonomia hanno maggior valore quando si decide di avanzare.

## Tutor override

Il tutor può sovrascrivere una decisione, ma deve lasciare una breve ragione. L'override non cancella le evidenze e non viene reinterpretato come prova di padronanza.

## Spiegabilità minima

Ogni decisione deve poter essere resa in forma umana:

```text
Decisione: recover
Obiettivo sospeso: proporzioni
Recupero: rapporti
Perché: il prodotto incrociato è eseguito correttamente quando la proporzione è già impostata,
ma 4/5 errori riguardano la costruzione del rapporto e la stessa difficoltà compare in un task senza formula.
Confidenza: 0.79
Ritorno a proporzioni: dopo due evidenze indipendenti di interpretazione corretta del rapporto.
```

## Limiti v0.1

Il motore v0.1 è intenzionalmente conservativo:

- non usa machine learning addestrato sui ragazzi;
- non produce diagnosi cliniche;
- non ottimizza su un solo punteggio;
- non decide sulla base di dati personali non necessari;
- non sostituisce il giudizio del tutor.

È un motore di decisione **trasparente e versionato**, progettato per diventare più sofisticato mantenendo leggibili le ragioni delle scelte.