# Tutor Experience + Hub Scuola Contract v1.0

## Scopo

TutorLab espone un facade applicativo stabile sopra target selection, Adaptive Engine, Session Engine e result transition. Hub Scuola resta proprietario di identità, persistenza e interfaccia; TutorLab riceve uno stato didattico e restituisce decisioni, sessioni ed aggiornamenti strutturati.

## Comando tutor

Il contratto supporta quattro intenti:

- `continue`: prosegue il percorso adattivo;
- `lesson`: prepara una sessione didattica sul target selezionato;
- `practice`: privilegia consolidamento/pratica ma non può saltare un prerequisito noto;
- `assessment`: verifica il working target selezionato, incluso un prerequisito quando il gate curricolare lo richiede.

Il tutor può inoltre impostare:

- target esplicito;
- durata tra 10 e 120 minuti;
- challenge band massima 1-5;
- `quantity_hint` tra 1 e 30;
- Student View on/off;
- note applicative brevi.

## Quantity hint

`quantity_hint` è un obiettivo best-effort, non un ordine di duplicare esercizi.

Il Session Engine:

1. costruisce sempre il minimo strutturale richiesto dalla pedagogia dell'azione;
2. aggiunge task soprattutto a pratica autonoma/guidata, verifica e transfer;
3. conserva fingerprint unici;
4. si ferma se la famiglia non offre altra varietà;
5. espone `task_quantity_requested`, `task_quantity_actual`, `task_quantity_shortfall` e `task_quantity_satisfied`.

## Contratto Hub Scuola

Input minimo:

- `student_ref.external_id`: riferimento opaco gestito da Hub Scuola;
- `learning_snapshot`: stato didattico TutorLab;
- `request`: comando tutor.

Output planning:

- selection root/working target;
- decisione adattiva e azione finale;
- objective stack;
- sessione Tutor View;
- Student View sanitizzata.

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

Sono versionati nel runner locale:

- `tools/check_tutor_contract_schemas.py`;
- `tools/check_tutor_service.py`.

Nel runtime disponibile sono stati eseguiti con esito positivo:

- JSON Schema Draft 2020-12 reali del branch, inclusi casi negativi;
- compilazione dei file runtime modificati;
- regressione eseguibile su `session_engine.py` e `tutor_service.py` con dipendenze controllate;
- comportamento legacy del Session Engine senza `quantity_hint`;
- quantity hint, fingerprint e Student View;
- determinismo;
- priorità dei prerequisiti in practice;
- assessment del prerequisito selezionato;
- immutabilità dello snapshot;
- protezione cross-subject.

Il container usato in questa sessione non dispone di uscita HTTPS verso GitHub, quindi non può effettuare `git clone` del repository e non può eseguire il runner cumulativo sul checkout completo. `tools/run_local_validation.py` resta il comando canonico per quell'esecuzione in un ambiente con checkout locale.

## Costi CI

Nessun GitHub Actions workflow fa parte di questo contratto. Le verifiche restano locali/manuali.
