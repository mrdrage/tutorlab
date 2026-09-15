# Tutor Experience + Hub Scuola Contract v1.0

## Scopo

TutorLab espone un facade applicativo stabile sopra target selection, Adaptive Engine, Session Engine e result transition. Hub Scuola resta proprietario di identità, persistenza e interfaccia; TutorLab riceve uno stato didattico e restituisce decisioni, sessioni ed aggiornamenti strutturati.

## Comando tutor

Il contratto supporta quattro intenti:

- `continue`: prosegue il percorso adattivo;
- `lesson`: prepara una sessione didattica sul target selezionato;
- `practice`: privilegia consolidamento/pratica ma non può saltare un prerequisito noto;
- `assessment`: verifica il working target selezionato, incluso un prerequisito quando il gate curricolare lo richiede.

Il tutor può inoltre impostare target esplicito, durata tra 10 e 120 minuti, challenge band massima 1-5, `quantity_hint` tra 1 e 30, Student View on/off e note applicative brevi.

## Quantity hint

`quantity_hint` è un obiettivo best-effort, non un ordine di duplicare esercizi. Il Session Engine costruisce sempre il minimo strutturale richiesto dalla pedagogia dell'azione, aggiunge task soprattutto a pratica, verifica e transfer, conserva fingerprint unici, si ferma quando la varietà disponibile è esaurita ed espone `task_quantity_requested`, `task_quantity_actual`, `task_quantity_shortfall` e `task_quantity_satisfied`.

## Contratto Hub Scuola

Input minimo: `student_ref.external_id`, `learning_snapshot` e `request`.

Output planning: selection root/working target, decisione adattiva e azione finale, objective stack, sessione Tutor View e Student View sanitizzata.

Round-trip risultati:

`Hub Scuola -> session_result -> TutorLab -> evidence events -> snapshot update -> next step -> Hub Scuola`

TutorLab non conosce tabelle, account, login o schema storage di Hub Scuola.

## Guardrail

- lesson/practice non bypassano lacune di prerequisito note;
- assessment testa il working target selezionato;
- request sconosciute, tipi errati e materie non supportate sono rifiutati;
- planning non muta lo snapshot chiamante;
- una sessione non può aggiornare una materia differente;
- Student View rimuove solution, rubric, error signals e generation parameters;
- snapshot/request/seed uguali producono la stessa sessione.

## Validazione

Sono versionati nel runner locale `tools/check_tutor_contract_schemas.py` e `tools/check_tutor_service.py`.

Nel runtime disponibile sono stati eseguiti con esito positivo i JSON Schema Draft 2020-12 reali del branch, inclusi casi negativi, la compilazione dei file runtime modificati e una regressione eseguibile sui file reali `session_engine.py` e `tutor_service.py` con dipendenze controllate. La regressione ha verificato comportamento legacy senza `quantity_hint`, quantità, fingerprint, Student View, determinismo, priorità dei prerequisiti, assessment, immutabilità dello snapshot e protezione cross-subject.

Il container usato in questa sessione non dispone di uscita HTTPS verso GitHub, quindi non può effettuare `git clone` del repository. Il runner cumulativo `tools/run_local_validation.py` resta il comando canonico per un ambiente con checkout completo. Il merge v1.0 si basa quindi sulla suite storica già chiusa nei macro-blocchi v0.x più la regressione mirata e gli schema test dei soli confini runtime modificati in v1.0.

## Costi CI

Nessun GitHub Actions workflow fa parte di questo contratto. Le verifiche restano locali/manuali.
