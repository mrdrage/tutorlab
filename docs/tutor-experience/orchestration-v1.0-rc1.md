# Tutor Orchestration v1.0-rc1

## Obiettivo

Tutor Orchestration trasforma il motore didattico di TutorLab in un contratto utilizzabile da un tutor, da Hub Scuola o da una futura Skill senza duplicare la logica pedagogica.

Il facade non interpreta il linguaggio naturale. Una UI, ChatGPT o un adapter converte la richiesta umana in un `TutorRequest` strutturato. TutorLab resta deterministico.

```text
richiesta tutor / UI
        ↓
TutorRequest
        ↓
select_target → objective stack → decision → session dispatch
        ↓
TutorPackage
        ↓
Tutor View / Student View
        ↓
SessionResult
        ↓
evidence → Learning Snapshot → next step
        ↓
TutorTransition
```

## Contratti

### TutorRequest

Campi principali:

- `subject`: mathematics, english, italian, french, spanish;
- `requested_target_id`: opzionale;
- `duration_minutes`: 10-120;
- `intent`: adaptive, practice, assessment, diagnostic;
- `max_challenge_band`: 1-5;
- `output`: both, tutor, student;
- `seed`: consente riproducibilità.

I default di durata e challenge band provengono dal Learning Snapshot quando disponibili.

### TutorPackage

Contiene:

- richiesta normalizzata;
- target radice e target di lavoro;
- objective stack da persistere;
- azione scelta e motivazione;
- sessione completa interna;
- Tutor View;
- Student View;
- eventuale `needs_review` se manca capability generativa.

Il package completo è un envelope trusted. La sessione interna contiene anche dati necessari a scoring, feedback e persistenza. **Solo `views.student` è student-safe.**

### TutorTransition

Dopo la sessione restituisce:

- evidence events;
- Learning Snapshot aggiornato;
- task che richiedono scoring esterno;
- next step;
- riepilogo sintetico per il tutor.

`complete_tutor_session` applica internamente lo stack prodotto da `prepare_tutor_package`, così l'integrazione non può dimenticare il passaggio di planning.

## Semantica degli intent

### adaptive

TutorLab usa stato, errori, prerequisiti e curriculum per decidere tra recover, consolidate, advance, extend e reassess.

Esempio umano: `Preparami 40 minuti di matematica.`

### practice

Il tutor chiede pratica mirata. TutorLab mantiene il routing dei prerequisiti ma genera una sessione di consolidamento sul target di lavoro.

Esempio umano: `Fammi esercitare sul Present Simple.`

### assessment

Genera una sessione senza supporto orientata a raccogliere nuova evidenza sul target di lavoro.

Esempio umano: `Domani ha la verifica sulle proporzioni: fammi una prova.`

### diagnostic

Usa anch'esso una sessione di reassessment, ma conserva l'intento diagnostico nel contratto perché l'applicazione chiamante può presentarlo e trattarlo diversamente.

Esempio umano: `Continua a sbagliare le frazioni: trova il problema.`

Assessment e diagnostic condividono oggi la forma di sessione `reassess`; non sono però sinonimi a livello di prodotto.

## Precedenza del tutor

Senza `requested_target_id`, un objective stack attivo viene ripreso. Se non esiste, il motore individua il curriculum frontier.

Con un target esplicito, la richiesta del tutor prevale sullo stack precedente. Il nuovo target resta comunque soggetto ai gateway didattici: una lacuna nota o un prerequisito senza evidenza può diventare temporaneamente il working target.

Questa regola distingue due concetti:

- **override del tutor**: sceglie l'obiettivo radice;
- **sicurezza didattica**: TutorLab può scendere a un prerequisito prima di affrontarlo.

## Advance e objective stack

Quando una decisione radice produce `advance`, il nuovo objective stack viene ricreato sul successore. Target della sessione e target persistito non possono divergere.

Dopo un recupero, invece, `complete_current()` risale allo stack sospeso e il target viene rivalutato prima di continuare.

## Separazione Tutor / Student

La Student View rimuove almeno:

- soluzioni;
- rubriche;
- error signals;
- generation parameters;
- history fingerprints.

L'intero `TutorPackage` non deve mai essere inoltrato direttamente allo studente.

## Linguaggio naturale

Il core non contiene regex, classificatori o prompt per interpretare frasi libere. La trasformazione deve avvenire nello strato chiamante.

Esempi:

```text
"Preparami 40 minuti di matematica"
→ {subject: mathematics, duration_minutes: 40, intent: adaptive}

"Fammi esercitare sul Present Simple"
→ {subject: english, requested_target_id: eng.grammar.present_simple, intent: practice}

"Fammi una verifica sulle proporzioni"
→ {subject: mathematics, requested_target_id: math.numbers.proportions, intent: assessment}

"Trova perché continua a sbagliare le frazioni"
→ {subject: mathematics, requested_target_id: math.numbers.fraction-operations, intent: diagnostic}
```

Questo permette di cambiare UI, modello linguistico o integrazione senza cambiare il motore didattico.

## Non-obiettivi di rc1

- autenticazione;
- database;
- identificazione anagrafica dello studente;
- UI web;
- stampa/PDF;
- parsing naturale nel core;
- modifica diretta del database di Hub Scuola.

Questi appartengono agli adapter e ai prodotti che consumano TutorLab.
