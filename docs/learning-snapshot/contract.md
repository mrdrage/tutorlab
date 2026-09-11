# Contratto TutorLab v0.1

Il contratto applicativo e composto da due operazioni logiche.

## Plan

Input minimo:

- Learning Snapshot;
- subject;
- target richiesto opzionale;
- durata opzionale;
- seed di generazione.

Output:

- `selection`: root target, working target e motivo;
- `objective_stack`;
- `decision`: azione adattiva e motivazione;
- `status`: `ok` oppure `needs_review`;
- `session`: presente solo quando esiste una task family registrata;
- eventuale capability warning.

## Transition

Input minimo:

- Learning Snapshot usato per la sessione;
- subject;
- sessione;
- session result.

Output:

- evidence events prodotti dalla sessione;
- Learning Snapshot aggiornato;
- pending task che richiedono scoring esterno;
- next step;
- objective stack aggiornato.

## Regola di integrazione

TutorLab non decide come o dove persistire lo snapshot. Un adapter esterno puo salvarlo, versionarlo o ricostruirlo da uno storico piu ampio. Il core resta deterministico e indipendente dall'applicazione chiamante.

## Compatibilita

Ogni payload strutturato porta una versione. Modifiche incompatibili richiederanno un incremento della versione del contratto invece di cambiare silenziosamente il significato dei campi.
