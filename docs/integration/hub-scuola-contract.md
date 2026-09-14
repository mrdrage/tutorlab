# TutorLab ↔ Hub Scuola: contratto di integrazione

## Responsabilità

**Hub Scuola** gestisce identità, persistenza, storico applicativo e interfaccia del tutor.

**TutorLab** gestisce curriculum, prerequisiti, stato didattico strutturato, decisione adattiva, generazione della sessione, evidence events e next step.

L'integrazione non deve spostare logica didattica dentro Hub Scuola né trasformare TutorLab in un database studenti.

## Privacy by design

TutorLab non richiede nome, cognome, email, data di nascita o altri dati identificativi per decidere una sessione.

Un adapter può associare esternamente un riferimento opaco, ad esempio:

```json
{
  "learner_ref": "hub:student:opaque-id",
  "snapshot_revision": 42,
  "snapshot": {}
}
```

`learner_ref` e `snapshot_revision` appartengono all'envelope dell'applicazione e non al core didattico.

## Operazione 1: Prepare

Input applicativo minimo:

```text
Learning Snapshot + TutorRequest
```

TutorLab restituisce un `TutorPackage` con:

- selection;
- objective stack;
- plan;
- sessione interna;
- Tutor View;
- Student View;
- patch di planning;
- status/capability warning.

Hub può mostrare il brief al tutor e la sola `views.student` allo studente.

## Operazione 2: Complete

Dopo la sessione Hub invia:

```text
snapshot usato per Prepare + TutorPackage + SessionResult
```

TutorLab verifica l'identità della sessione, applica la patch di planning, converte i risultati in evidence events e restituisce un `TutorTransition`.

Il transition contiene:

- snapshot aggiornato;
- evidence events;
- next step;
- pending scoring;
- tutor summary.

Hub persiste il risultato come nuova revisione.

## Concorrenza e revisioni

Il core non implementa locking. L'adapter Hub dovrebbe usare una revisione ottimistica:

1. legge snapshot revision N;
2. chiama Prepare;
3. completa la sessione;
4. salva TutorTransition soltanto se la revisione corrente è ancora N;
5. in caso di conflitto ricarica lo snapshot e rivaluta invece di sovrascrivere evidenze più recenti.

## Pending scoring

Alcuni task aperti possono richiedere valutazione del tutor o di uno strato esterno. In quel caso `pending_task_ids` non è vuoto.

Hub non deve inventare punteggi mancanti. Può raccogliere lo scoring e completare il flusso quando le evidenze necessarie sono disponibili.

## Capability boundary

Se TutorLab conosce un obiettivo ma non dispone di una task family eseguibile, il package restituisce `status: needs_review` e non contiene una sessione utilizzabile.

Hub deve mostrare il warning al tutor. Non deve sostituire silenziosamente l'obiettivo né generare esercizi con una logica alternativa.

## Student safety boundary

Il `TutorPackage` completo è trusted/internal. Può contenere soluzioni, rubriche e informazioni diagnostiche.

La superficie studente ammessa è esclusivamente:

```text
TutorPackage.views.student
```

Una UI deve trattare questa separazione come un confine di sicurezza, non come una scelta grafica.

## Cosa persistere

Hub dovrebbe conservare almeno:

- Learning Snapshot aggiornato o dati sufficienti a ricostruirlo;
- session id;
- evidence events;
- next step;
- timestamp applicativi;
- eventuale relazione con materiali/PDF prodotti;
- revisione dello snapshot.

I fingerprint possono restare nello snapshot per impedire ripetizioni involontarie.

## Cosa non reimplementare

Hub non deve avere una seconda copia di:

- prerequisite routing;
- mastery thresholds;
- recover/consolidate/advance/extend/reassess;
- objective stack;
- Difficulty Engine;
- curriculum frontier;
- regole di ritorno dopo recovery.

Queste appartengono a TutorLab e vengono consumate attraverso i contratti versionati.

## Flusso completo

```text
Hub storage
   ↓ load snapshot + revision
ChatGPT/Hub UI → TutorRequest
   ↓
TutorLab.prepare
   ↓
TutorPackage
   ↓                    ↘ Tutor View
Student View → attività
   ↓
SessionResult
   ↓
TutorLab.complete
   ↓
TutorTransition
   ↓
Hub optimistic persistence
```

Questo contratto permette a TutorLab di restare indipendente dalla UI e dal database, e a Hub Scuola di diventare la memoria applicativa senza appropriarsi della pedagogia.
