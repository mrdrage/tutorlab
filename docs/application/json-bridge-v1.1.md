# TutorLab JSON Bridge v1.1

## Scopo

Il bridge JSON rende il facade applicativo di TutorLab invocabile da un processo esterno senza introdurre dipendenze da database, autenticazione, UI o runtime specifici di Hub Scuola.

Il protocollo usa JSON su `stdin` e `stdout`. Hub Scuola resta proprietario di identità e persistenza; TutorLab resta proprietario delle decisioni didattiche, della generazione delle sessioni e dell'interpretazione dei risultati.

La release TutorLab è `v1.1`; la prima versione del protocollo bridge è `bridge_version = "1.0"`. Il contratto Hub Scuola contenuto nel payload resta `version = "1.0"`. Le due versioni sono separate intenzionalmente.

## Envelope

Ogni richiesta al bridge è un oggetto JSON con:

- `bridge_version`: attualmente `"1.0"`;
- `operation`: `plan` oppure `transition`;
- `payload`: oggetto conforme al contratto Hub Scuola v1.0;
- `seed`: intero opzionale usato soltanto da `plan`, default `1`.

Campi sconosciuti vengono rifiutati. `seed` non è ammesso per `transition`.

Successo:

```json
{
  "bridge_version": "1.0",
  "ok": true,
  "result": {}
}
```

Errore:

```json
{
  "bridge_version": "1.0",
  "ok": false,
  "error": {
    "code": "INVALID_PAYLOAD",
    "type": "BridgeProtocolError",
    "message": "payload must be an object"
  }
}
```

`error.code` è il campo stabile per i client. `error.type` e `error.message` servono al debug e non devono essere usati come contratto applicativo.

Codici previsti:

- `EMPTY_REQUEST`;
- `INVALID_JSON`;
- `INVALID_ENVELOPE`;
- `INVALID_PAYLOAD`;
- `INVALID_SEED`;
- `UNSUPPORTED_BRIDGE_VERSION`;
- `UNSUPPORTED_OPERATION`;
- `TUTORLAB_VALIDATION_ERROR`;
- `INTERNAL_ERROR`.

Gli errori applicativi e di parsing vengono serializzati nel protocollo; il bridge non emette traceback su `stdout`.

## JSON Schema

Il protocollo è descritto da:

- `schemas/tutor-service-bridge-request.schema.json`;
- `schemas/tutor-service-bridge-response.schema.json`.

Lo schema della request distingue `plan` e `transition`: il planning richiede una request TutorLab nel payload e può ricevere `seed`; la transition richiede `session_result`, `metadata.subject` e `metadata.session` e non accetta `seed`.

Il runtime non dipende da `jsonschema`. Gli schema sono un contratto verificabile per integrazione e test, mentre il bridge mantiene validazione runtime leggera e autonoma.

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

`tools/check_tutor_service_bridge_schemas.py` verifica la validità Draft 2020-12 dei due schema bridge e casi positivi/negativi degli envelope.

`tools/check_tutor_service_bridge.py` verifica:

- planning riuscito tramite processo separato;
- `bridge_version` su ogni risposta;
- determinismo con snapshot/request/seed uguali;
- immutabilità dello snapshot in planning;
- round-trip `plan -> transition`;
- produzione di evidence, snapshot update e next step;
- protezione cross-subject;
- codici errore stabili;
- operazioni sconosciute;
- versione bridge non supportata;
- campi envelope sconosciuti;
- payload mancante;
- seed non valido e seed vietato su transition;
- request JSON non-object;
- JSON malformato;
- input vuoto;
- assenza di output diagnostico su `stderr` nei casi gestiti.

Entrambi i controlli sono inclusi nel runner canonico `tools/run_local_validation.py`.

## Vincoli

- nessun dato reale degli studenti nel repository;
- nessuna dipendenza da Hub Scuola nel motore;
- nessun GitHub Actions workflow richiesto;
- validazioni locali/manuali.
