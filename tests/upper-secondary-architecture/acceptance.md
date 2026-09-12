# Upper Secondary Architecture v0.7 — acceptance criteria

Il macro-blocco è accettabile solo con validazioni locali/manuali. `.github/workflows` deve restare assente.

## Modello dati

- `school_stage` distingue `middle_school` e `upper_secondary`.
- `stage_year` arriva a 5 ma un profilo quadriennale deve rifiutare il quinto anno.
- il percorso scolastico è separato dallo stato di padronanza dello studente;
- il catalogo distingue almeno liceo, tecnico e professionale;
- sono rappresentabili indirizzo, articolazione, opzione, specializzazione e anno di scelta;
- `duration_years` non è hard-coded a 5;
- una variante quadriennale è distinguibile da quella standard;
- fonti e validità temporale sono versionate;
- riferimenti a fonti inesistenti devono essere rifiutati dal controllo locale.

## Compatibilità

- uno snapshot legacy senza `academic_context` continua a essere interpretato come `middle_school` usando `typical_year`;
- i curriculum e i generatori delle medie non vengono rinominati;
- gli ID esistenti restano validi;
- il target selector usa il resolver superiore soltanto quando il contesto dichiara `upper_secondary`;
- il capability boundary resta prudente: conoscere la struttura delle superiori non significa avere già generation coverage v0.8.

## Grafo

- i nodi superiori usano namespace `<subject>.us.*`;
- un prerequisito può puntare a un nodo delle medie;
- ogni prerequisito dei gateway v0.7 deve risolversi in un nodo realmente esistente;
- common core, family core e profile overlay devono comporsi senza duplicare ID;
- un overlay liceale non deve apparire in un tecnico o professionale;
- un overlay tecnico non deve apparire in un liceo o professionale;
- `stage_year` filtra i nodi senza essere confuso con il Difficulty Engine.

## Casi minimi

### Liceo scientifico
Deve ricevere i gateway comuni di matematica più `math.us.gateway.scientific-reasoning`, ma non `math.us.gateway.technical-modelling`.

### Tecnico Informatica
Deve ricevere i gateway comuni di matematica più `math.us.gateway.technical-modelling`, ma non il gateway specifico dello scientifico.

### Professionale Manutenzione
Deve ricevere il common core, senza gli overlay dei due casi precedenti.

### Inglese
Il gateway A2 deve essere comune ai profili seed e preparare la futura progressione B1/B2 senza dichiararla già implementata.

### Quadriennale
`it.upper.tecnico-informatica-4y` con anno 4 è valido; anno 5 è invalido.

## Validazione locale

`python3 tools/check_upper_secondary_architecture.py`

deve terminare con exit code 0 prima del merge. Il runner `tools/run_local_validation.py` deve includere questo controllo, ma non deve essere eseguito tramite GitHub Actions.
