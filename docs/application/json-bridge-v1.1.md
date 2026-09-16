# TutorLab JSON Bridge v1.1

## Scopo

Il bridge JSON rende il facade applicativo di TutorLab invocabile da un processo esterno senza introdurre dipendenze da database, autenticazione, UI o runtime specifici di Hub Scuola.

Il protocollo usa JSON su `stdin` e `stdout`. Hub Scuola resta proprietario di identità e persistenza; TutorLab resta proprietario delle decisioni didattiche, della generazione delle sessioni e dell'interpretazione dei risultati.

## Envelope

Ogni richiesta al bridge è un oggetto JSON con:

- `operation`: `plan` oppure `transition`;
- `payload`: oggetto conforme al contratto Hub Scuola v1.0;
- `seed`: intero opzionale usato soltanto da `plan`, default `1`.

Successo:

```json
{"ok": true, "result": {}}
```

Errore:

```json
{"ok": false, "error": {"type": "ValueError", "message": "..."}}
```

Gli errori applicativi e di parsing vengono serializzati nel protocollo; il bridge non emette traceback su `stdout`.

## Planning

`operation = "plan"` inoltra il payload a `hub_plan`.

Il payload minimo contiene:

- `version = "1.0"`;
- `student_ref.external_id` opaco e fittizio nei test;
- `learning_snapshot`;
- `request` TutorLab.

L'output contiene `student_ref` e `plan`, inclusi selection, decision, `objective_stack`, Tutor View e Student View.

Il planning non modifica il `learning_snapshot` ricevuto.

### Persistenza dell'objective stack

Prima di registrare il risultato della sessione, il client deve persistere nel Learning Snapshot l'`objective_stack` restituito dal planning. Questa responsabilità resta lato Hub Scuola perché Hub possiede lo storage.

TutorLab non scrive direttamente su database e non conserva stato tra due invocazioni del bridge.

## Transition

`operation = "transition"` inoltra il payload a `hub_transition`.

Il payload contiene:

- `version = "1.0"`;
- lo stesso `student_ref`;
- il Learning Snapshot aggiornato con l'objective stack del planning;
- `session_result`;
- `metadata.subject`;
- `metadata.session`, cioè la sessione Tutor View prodotta dal planning.

L'output contiene:

- evidence events;
- snapshot update;
- next step didattico.

Una sessione non può essere applicata a una materia diversa da quella per cui è stata generata.

## Proprietà verificate

`tools/check_tutor_service_bridge.py` verifica:

- planning riuscito tramite processo separato;
- determinismo con snapshot/request/seed uguali;
- immutabilità dello snapshot in planning;
- round-trip `plan -> transition`;
- produzione di evidence, snapshot update e next step;
- protezione cross-subject;
- operazioni sconosciute;
- payload mancante;
- seed non valido;
- request JSON non-object;
- JSON malformato;
- input vuoto;
- assenza di output diagnostico su `stderr` nei casi gestiti.

Il controllo è incluso nel runner canonico `tools/run_local_validation.py`.

## Vincoli

- nessun dato reale degli studenti nel repository;
- nessuna dipendenza da Hub Scuola nel motore;
- nessun GitHub Actions workflow richiesto;
- validazioni locali/manuali.
