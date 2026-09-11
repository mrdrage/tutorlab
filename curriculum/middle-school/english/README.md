# Inglese — scuola secondaria di primo grado

TutorLab rappresenta l'inglese come **grafo di competenze comunicative e prerequisiti**, non come una sequenza di unità grammaticali.

## Obiettivo

Portare progressivamente lo studente verso il livello **A2 QCER** al termine della terza media, come previsto dalle Indicazioni nazionali per la scuola secondaria di primo grado, mantenendo separati:

1. il quadro curricolare ufficiale;
2. la progressione tipica TutorLab;
3. il percorso effettivo del singolo studente.

La classe indica quindi il momento tipico in cui una competenza viene affrontata, ma non impedisce a TutorLab di recuperare un prerequisito di un anno precedente o anticipare un'attività già accessibile.

## Architettura linguistica

Il modello segue la logica QCER: la lingua è azione comunicativa. Il curriculum non misura soltanto la conoscenza di regole, ma collega i sistemi linguistici alle attività reali di comunicazione.

### Sistemi abilitanti

- `grammar`
- `vocabulary`
- `phonology`

Questi nodi forniscono strumenti. Non costituiscono da soli padronanza comunicativa.

### Uso della lingua

- `reading`
- `listening`
- `spoken_interaction`
- `spoken_production`
- `writing`
- `mediation`

Il CEFR Companion Volume organizza infatti le attività comunicative in reception, production, interaction e mediation. TutorLab mantiene queste dimensioni distinte affinché uno studente possa, per esempio, comprendere bene una struttura in lettura ma non riuscire ancora a usarla autonomamente in conversazione.

### Competenze trasversali

- `intercultural`
- `learning_strategies`

Comprendono consapevolezza pragmatica e culturale, strategie di comprensione, richiesta di chiarimenti, riparazione della comunicazione, autovalutazione e uso consapevole delle risorse.

## Progressione QCER

I soli livelli ufficiali usati come ancoraggio sono `A1` e `A2`.

TutorLab aggiunge una **progressione interna**, che non va interpretata come una nuova scala QCER:

- `A1_core` — competenze fondamentali A1;
- `A1_to_A2` — ponte didattico verso A2;
- `A2_core` — competenze centrali A2;
- `A2_extension` — consolidamento avanzato o ponte verso il ciclo successivo.

Queste etichette servono al motore adattivo e non sono certificazioni linguistiche.

## Regola fondamentale

Una struttura grammaticale è considerata realmente disponibile solo quando compare in evidenze d'uso coerenti.

Esempio: conoscere la forma del Present Simple non equivale a saper parlare della propria routine. TutorLab può distinguere:

- regola conosciuta;
- forma riconosciuta in lettura/ascolto;
- produzione controllata corretta;
- uso autonomo in interazione;
- uso stabile in contesti diversi.

## Progressione tipica

### 1ª media

Consolidamento A1 e costruzione della base comunicativa: identità, famiglia, scuola, routine, casa, città, tempo libero, cibo; `be`, `have got`, Present Simple, prime domande, `can`, `there is/are`, Present Continuous; lettura e ascolto di messaggi semplici; interazioni brevi e scrittura personale essenziale.

### 2ª media

Ponte A1→A2: racconto del passato, confronto, quantità, obbligo e consiglio, programmi e intenzioni; viaggi, acquisti, salute, luoghi e ambiente; testi e ascolti più estesi; transazioni quotidiane, narrazioni semplici, email informali e prime attività sistematiche di mediazione.

### 3ª media

Consolidamento A2: esperienze, futuro, ipotesi semplici, opinioni, tecnologia, ambiente, lavoro e cultura; reading/listening A2, interazione per pianificare e risolvere problemi, brevi presentazioni, testi connessi, mediazione e strategie di autonomia. Alcune strutture tipiche dei manuali di terza sono marcate `extension` quando non sono necessarie per dimostrare A2.

## INVALSI

INVALSI grado 8 rileva soltanto **Reading e Listening**, con task A1 e A2. TutorLab usa queste prove come una fonte importante per calibrare la comprensione, ma non riduce il curriculum a ciò che viene standardizzato: speaking, writing, interaction e mediation restano parti essenziali del profilo linguistico.

## File

- `year-1.json` — consolidamento A1;
- `year-2.json` — ponte A1→A2;
- `year-3.json` — consolidamento A2;
- `cross-year-links.json` — gateway e regole di recupero;
- `map.md` — vista sintetica per il tutor;
- `cefr-mapping.md` — corrispondenza tra architettura TutorLab e QCER;
- `sources.md` — fonti ufficiali e politica di versionamento.

## Stato

Versione curriculum: **0.1.0**

Il curriculum definisce l'ossatura delle competenze. Famiglie di esercizi, session engine e decision engine verranno innestati su questo grafo nei macro-blocchi successivi.
