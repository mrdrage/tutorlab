# TutorLab Roadmap

## Stato dei macro-blocchi

- [x] **Fondazioni pedagogiche + Difficulty Engine v0.1**
- [x] **Curriculum Matematica 1ª-3ª media + grafo dei prerequisiti v0.1**
- [x] **Curriculum Inglese 1ª-3ª media + progressione A1-A2**
- [x] **Motore adattivo: diagnosi, errori e decisione del passo successivo**
- [x] **Generazione di sessioni didattiche complete e criteri di qualità**
- [x] **Learning Snapshot + contratto applicativo per futura integrazione Hub Scuola**
- [x] **Generation Coverage v0.2: intera 1ª media eseguibile per Matematica e Inglese**

I macro-blocchi sono l'unità di avanzamento del progetto. Le attività interne possono essere granulari, ma un blocco è completo solo quando produce un sottosistema coerente, documentato e verificabile.

## v0.1 — Fondazioni

Obiettivo: dimostrare un circuito didattico coerente, eseguibile e rappresentabile in dati strutturati.

Completato: pedagogia comune, Difficulty Engine, curriculum Matematica e Inglese, grafi dei prerequisiti, Adaptive Engine, Session Engine, vertical slice, evidence events, objective stack, Learning Snapshot, target selection, capability boundary e CI.

Non-obiettivi: UI completa, database applicativo, login/account, integrazione diretta con Hub Scuola, generazione massiva di PDF e riproduzione di manuali protetti da copyright.

## v0.2 — Curriculum e prerequisiti

- [x] grafi Matematica e Inglese;
- [x] fonti curricolari versionate;
- [x] relazioni prerequisito-obiettivo-successore;
- [ ] rubriche di padronanza più ricche per famiglie di competenze.

## v0.3 — Generazione controllata

- [x] famiglie di esercizi parametrizzate;
- [x] separazione tra contenuto, difficoltà e guida;
- [x] vincoli anti-ripetizione;
- [x] quality gate e vertical slice;
- [x] generation coverage completa dei nodi di 1ª media per Matematica e Inglese;
- [x] CI che impedisce regressioni di copertura quando cambia il curriculum di 1ª;
- [ ] generation coverage di 2ª media;
- [ ] generation coverage di 3ª media.

## v0.4 — Adattamento e Learning Snapshot

- [x] modello di sessione e risultato;
- [x] evidence events e stato di competenza;
- [x] decision engine;
- [x] objective stack;
- [x] target selector;
- [x] capability boundary curriculum/generazione;
- [x] Learning Snapshot;
- [x] contratto applicativo Plan / Transition;
- [x] fixture sintetiche e CI.

## v0.5 — Nuove materie

Portare il framework comune su almeno due discipline non isomorfe alla matematica:

- Italiano;
- una tra Scienze, Storia o Geografia.

Obiettivo: verificare che l'architettura sia realmente multidisciplinare.

## v0.6 — Esperienza Tutor

- comandi ad alto livello, es. «preparami 40 minuti»;
- output pronto per lezione;
- modalità diagnosi, recupero, verifica e ripasso;
- controllo esplicito di tempo, difficoltà e quantità;
- esportazione strutturata delle evidenze.

## v0.7 — Integrazione Hub Scuola

- adapter tra storage Hub Scuola e Learning Snapshot;
- uso del contratto Plan / Transition senza accoppiare le UI;
- persistenza di attività, evidenze e prossimo obiettivo lato applicazione;
- TutorLab indipendente dal database di Hub Scuola.

## v1.0 — TutorLab stabile

TutorLab 1.0 deve poter ricevere uno stato didattico, scegliere un obiettivo coerente, verificare prerequisiti, costruire una sessione, interpretare i risultati, proporre il passo successivo e motivare ogni decisione in modo verificabile dal tutor.
