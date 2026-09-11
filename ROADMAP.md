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

## v0.6 — Nuove materie

Portare il framework comune su almeno due discipline non isomorfe alla matematica:

- Italiano;
- una tra Scienze, Storia o Geografia.

Obiettivo: verificare che l'architettura sia realmente multidisciplinare.

## v0.7 — Esperienza Tutor

- comandi ad alto livello, es. «preparami 40 minuti»;
- output pronto per lezione;
- modalità diagnosi, recupero, verifica e ripasso;
- controllo esplicito di tempo, difficoltà e quantità;
- esportazione strutturata delle evidenze.

## v0.8 — Integrazione Hub Scuola

- adapter tra storage Hub Scuola e Learning Snapshot;
- uso del contratto Plan / Transition senza accoppiare le UI;
- persistenza di attività, evidenze e prossimo obiettivo lato applicazione;
- TutorLab indipendente dal database di Hub Scuola.

## v1.0 — TutorLab stabile

TutorLab 1.0 deve poter ricevere uno stato didattico, scegliere un obiettivo coerente, verificare prerequisiti, costruire una sessione, interpretare i risultati, proporre il passo successivo e motivare ogni decisione in modo verificabile dal tutor.
