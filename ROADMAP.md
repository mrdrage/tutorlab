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
- [x] **Tutor Experience + Hub Scuola Contract v1.0: facade applicativo, comandi tutor e round-trip dati**

I macro-blocchi sono l'unità di avanzamento del progetto. Le attività interne possono essere granulari, ma un blocco è completo solo quando produce un sottosistema coerente, documentato e verificabile.

Le validazioni automatiche tramite GitHub Actions non fanno parte del progetto: i controlli vengono mantenuti come script locali/manuali per evitare costi di workflow.

## v1.0 — TutorLab stabile

TutorLab 1.0 può ricevere uno stato didattico, scegliere un obiettivo coerente, verificare prerequisiti, costruire una sessione, interpretare i risultati, proporre il passo successivo e motivare ogni decisione in modo verificabile dal tutor.

### Tutor Experience + Hub Scuola

- [x] comando tutor versionato `continue / lesson / practice / assessment`;
- [x] durata, challenge band, quantità e target espliciti;
- [x] prerequisiti adattivi prioritari rispetto a lesson/practice;
- [x] assessment sul working target selezionato;
- [x] quantity hint best-effort con anti-ripetizione e tracciamento requested/actual/shortfall;
- [x] Tutor View / Student View separate;
- [x] contratto Hub Scuola con `student_ref` opaco e Learning Snapshot;
- [x] round-trip plan → session → result → evidence → snapshot update → next step;
- [x] validazione runtime allineata allo schema e protezione cross-subject;
- [x] test di schema e regressione mirata dei componenti runtime modificati;
- [x] nessun GitHub Actions/Workflow.

### Nota di validazione

Il container di esecuzione non dispone di connettività HTTPS verso GitHub e non può effettuare un clone completo. Per v1.0 sono stati quindi eseguiti nel runtime i JSON Schema reali e una regressione eseguibile sui file runtime modificati (`session_engine.py` e `tutor_service.py`), includendo comportamento legacy senza `quantity_hint`, determinismo, priorità dei prerequisiti, assessment, quantità, fingerprint, Student View e protezione cross-subject. Il runner cumulativo resta versionato in `tools/run_local_validation.py` per esecuzione in un ambiente con checkout completo.
