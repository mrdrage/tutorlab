# TutorLab Roadmap

## Stato dei macro-blocchi

- [x] **Fondazioni pedagogiche + Difficulty Engine v0.1**
- [x] **Curriculum Matematica 1ª-3ª media + grafo dei prerequisiti v0.1**
- [x] **Curriculum Inglese 1ª-3ª media + progressione A1-A2**
- [x] **Motore adattivo: diagnosi, errori e decisione del passo successivo**
- [x] **Generazione di sessioni didattiche complete e criteri di qualità**
- [x] **Learning Snapshot + contratto applicativo per futura integrazione Hub Scuola**
- [x] **Generation Coverage v0.2: intera 1ª media eseguibile per Matematica e Inglese**
- [x] **Generation Coverage v0.3: intera 2ª media eseguibile per Matematica e Inglese**
- [x] **Generation Coverage v0.4: intera 3ª media eseguibile + triennio completo Matematica e Inglese**
- [x] **Reliability v0.5: simulazioni longitudinali + calibrazione mastery**
- [x] **Language Expansion v0.6: Italiano + Francese + Spagnolo, triennio completo**
- [x] **Upper Secondary Architecture v0.7: modello dati, percorsi, layer e ponti medie → superiori**
- [x] **Math + English Upper Secondary v0.8: copertura eseguibile 1ª-5ª superiore**
- [x] **Longitudinal Reliability v0.9: traiettorie medie → maturità**
- [ ] **Tutor Experience + Hub Scuola Contract v1.0**

I macro-blocchi sono l'unità di avanzamento del progetto. Le attività interne possono essere granulari, ma un blocco è completo solo quando produce un sottosistema coerente, documentato e verificabile.

Le validazioni automatiche tramite GitHub Actions non fanno parte del progetto: i controlli vengono mantenuti come script locali/manuali per evitare costi di workflow.

## v0.1 — Fondazioni

Obiettivo: dimostrare un circuito didattico coerente, eseguibile e rappresentabile in dati strutturati.

Completato: pedagogia comune, Difficulty Engine, curriculum Matematica e Inglese, grafi dei prerequisiti, Adaptive Engine, Session Engine, vertical slice, evidence events, objective stack, Learning Snapshot, target selection, capability boundary e validazioni locali.

Non-obiettivi: UI completa, database applicativo, login/account, integrazione diretta con Hub Scuola, generazione massiva di PDF e riproduzione di manuali protetti da copyright.

## v0.2 — Curriculum e prerequisiti

- [x] grafi Matematica e Inglese;
- [x] fonti curricolari versionate;
- [x] relazioni prerequisito-obiettivo-successore;
- [x] rubriche di padronanza/evidenza per famiglie di competenze.

## v0.3 — Generazione controllata

- [x] famiglie di esercizi parametrizzate;
- [x] separazione tra contenuto, difficoltà e guida;
- [x] vincoli anti-ripetizione;
- [x] quality gate e vertical slice;
- [x] generation coverage completa della 1ª media per Matematica e Inglese;
- [x] generation coverage completa della 2ª media per Matematica e Inglese;
- [x] generation coverage completa della 3ª media per Matematica e Inglese;
- [x] validazione locale cumulativa dell'intero triennio 1ª-3ª.

## v0.4 — Adattamento e Learning Snapshot

- [x] modello di sessione e risultato;
- [x] evidence events e stato di competenza;
- [x] decision engine;
- [x] objective stack;
- [x] target selector;
- [x] capability boundary curriculum/generazione;
- [x] Learning Snapshot;
- [x] contratto applicativo Plan / Transition;
- [x] fixture sintetiche e validazione locale.

## v0.5 — Reliability e calibrazione

- [x] profili sintetici longitudinali per Matematica e Inglese;
- [x] simulazione di più sessioni consecutive;
- [x] metriche per avanzamento prematuro, recupero, reassessment e dipendenza dal supporto;
- [x] criterio distinto di uscita dal recupero;
- [x] rivalutazione obbligatoria del target dopo il recupero;
- [x] decadimento delle ipotesi d'errore superate da evidenze successive;
- [x] contraddizione basata su alternanza recente non spiegata;
- [x] rubriche di sufficienza dell'evidenza per famiglie disciplinari;
- [x] confronto locale di configurazioni candidate senza modifica automatica della policy;
- [x] runner unico di validazione locale, senza GitHub Actions.

## v0.6 — Language Expansion

Obiettivo: dimostrare che l'architettura di TutorLab regge una lingua madre e due seconde lingue comunitarie senza duplicare il motore.

- [x] Language Core comune per ricezione, produzione, interazione, mediazione, risorse linguistiche e strategie;
- [x] Italiano 1ª-3ª media: 45 nodi curricolari eseguibili;
- [x] Francese 1ª-3ª media: 46 nodi, progressione interna verso A1;
- [x] Spagnolo 1ª-3ª media: 46 nodi, progressione interna verso A1;
- [x] schema curricolare linguistico unico per Inglese, Italiano, Francese e Spagnolo;
- [x] mastery rubric dedicate alle famiglie disciplinari e comunicative;
- [x] generation coverage completa dei 137 nuovi nodi;
- [x] 685 combinazioni adattive `recover/consolidate/advance/extend/reassess` nel controllo locale;
- [x] quality gate semantico sui worked example e materiale linguistico concreto;
- [x] controllo di diversità/fingerprint e separazione Tutor View / Student View;
- [x] vertical slice end-to-end per Italiano, Francese e Spagnolo fino a evidence/state/next step;
- [x] fonti MIM 2025 e QCER/CEFR versionate;
- [x] nessun GitHub Actions/Workflow.

## v0.7 — Upper Secondary Architecture

Obiettivo: rappresentare correttamente la secondaria di secondo grado prima di estendere i contenuti.

- [x] modello dati separato in `academic_context`, `education_pathway` e `curriculum_graph`;
- [x] `upper_secondary` come school stage mantenendo compatibilità con `middle_school`;
- [x] anni 1ª-5ª senza assumere che ogni percorso duri cinque anni;
- [x] percorsi standard e quadriennali tramite `duration_years` e `pathway_variant`;
- [x] licei, tecnici e professionali con indirizzo, articolazione, opzione/specializzazione quando pertinenti;
- [x] profili e fonti versionati per anno scolastico e stato di transizione;
- [x] curriculum componibile per layer: common core → family core → indirizzo → articolazione → opzione → profile;
- [x] namespace superiore `<subject>.us.*`;
- [x] prerequisiti verticali medie → superiori tramite gateway Math/English;
- [x] Learning Snapshot 0.2 con `academic_context` obbligatorio per gli snapshot 0.2 e compatibilità con snapshot legacy 0.1;
- [x] target selector stage-aware con fallback legacy invariato;
- [x] resolver di profilo/layer con controllo di durata, variante, validità temporale e deduplicazione;
- [x] capability boundary esplicito fra curriculum noto e generazione disponibile;
- [x] test locali per schema, composizione dei layer, quadriennali, prerequisiti verticali e retrocompatibilità;
- [x] nessun GitHub Actions/Workflow.

Il catalogo dei percorsi in v0.7 è un seed architetturale rappresentativo, non l'elenco territoriale esaustivo di ogni opzione attivata dalle singole scuole.

## v0.8 — Matematica + Inglese 1ª-5ª superiore

- [x] curriculum Matematica per common core e overlay liceali, scientifici, tecnici e professionali;
- [x] curriculum Inglese con progressione A2 bridge → B1/B1+ → B2 e linguaggio professionale/interculturale;
- [x] generation coverage completa dei 136 nodi superiori Math/English;
- [x] 680 combinazioni adattive `recover/consolidate/advance/extend/reassess` validate nel banco prova locale;
- [x] mastery rubric dedicate allo stage superiore;
- [x] generatori competency-aware per i nodi che richiedono allineamento semantico specifico;
- [x] quality gate su worked example, transfer, listening, diversità dei seed e Student View;
- [x] vertical slice end-to-end su Matematica scientifica e Inglese B2 fino a evidence/state/next step;
- [x] capability registry superiore attivata soltanto per nodi realmente generabili;
- [x] profili quinquennali e quadriennali attraversati dal resolver;
- [x] fonti MIM/QCER/INVALSI documentate con distinzione tra curriculum e assessment;
- [x] validazione locale/manuale senza workflow a pagamento.

La copertura v0.8 è verticale e componibile: i nodi comuni non vengono clonati per ogni indirizzo, mentre gli overlay modulano profondità, contesto e traguardi.

## v0.9 — Longitudinal Reliability 8-year

- [x] otto checkpoint consecutivi dalla 1ª media alla 5ª superiore per Matematica e Inglese;
- [x] profili forti, tipici, con gap cross-stage e dipendenza dal supporto;
- [x] recuperi che attraversano il confine medie → superiori;
- [x] recuperi annidati fino alla profondità massima 2 e ritorno ordinato nello stack;
- [x] rivalutazione del target sospeso dopo il recupero;
- [x] mastery calibrata su una finestra recente di 12 evidenze mantenendo lo storico lifetime;
- [x] confronto read-only di finestre candidate 0/12/18/24;
- [x] regressione sulla Reliability v0.5 e test specifico della evidence window;
- [x] metriche su avanzamento prematuro, falsi recuperi, loop, stagnazione, completion e support dependency;
- [x] 100 seed per profilo nel test di accettazione esteso;
- [x] nessun GitHub Actions/Workflow.

Nel banco prova sintetico equivalente v0.9 la configurazione scelta ha mantenuto premature advance sotto l'1%, cross-stage detection/return al 100%, deep recovery detection/return intorno al 93%, completion dei profili tipici al 100% e guardia support-dependent al 100%. Questi numeri sono metriche ingegneristiche sintetiche, non risultati su studenti reali.

## v1.0 — Tutor Experience + Hub Scuola Contract

Obiettivo: rendere TutorLab consumabile da un tutor o da Hub Scuola senza accoppiare il motore didattico a UI, database o autenticazione specifici.

- [x] schema versionato del comando tutor (`continue`, `lesson`, `practice`, `assessment`);
- [x] facade applicativo unico sopra target selector, Adaptive Engine, Session Engine e Transition;
- [x] separazione Tutor View / Student View preservata dal facade;
- [x] contratto Hub Scuola con `student_ref` opaco + Learning Snapshot;
- [x] ownership della persistenza esplicitata: Hub Scuola salva, TutorLab decide/genera/interpreta;
- [x] round-trip pianificazione → sessione → risultato → evidence → snapshot update → next step coperto da test;
- [x] precedenza dei prerequisiti sui comandi di lesson/practice;
- [x] semantica assessment: rivaluta il working target selezionato, anche quando è un prerequisito;
- [x] test di determinismo a snapshot/request/seed fissi e immutabilità dell'input;
- [x] schema test e integrazione nel runner locale;
- [ ] collaudo finale dell'intero runner sul checkout del branch;
- [ ] review/merge della PR v1.0;
- [x] nessun GitHub Actions/Workflow.

Il contratto v1.0 definisce un boundary applicativo, non una API HTTP. Trasporto, database, autenticazione, UI e PDF sono adapter esterni e non devono contaminare il motore didattico.

## Dopo v1.0

Una volta stabilizzato il contract applicativo, i passi successivi possono essere sviluppati come adapter separati:

- adapter Hub Scuola concreto sul formato dati reale;
- UI tutor per comandi ad alto livello;
- rendering/export di schede studente e vista tutor;
- eventuale servizio HTTP locale o plugin, senza cambiare la logica curricolare.
