# Learning Snapshot v0.1

Il Learning Snapshot e il confine tra TutorLab e una futura applicazione che conserva lo storico dello studente.

TutorLab resta un motore didattico: riceve uno snapshot, decide, genera una sessione e restituisce uno snapshot aggiornato. La persistenza applicativa resta esterna.

Il flusso e:

`snapshot -> target selection -> objective stack -> adaptive decision -> session dispatch -> result -> evidence -> updated snapshot -> next step`

Lo snapshot contiene solo informazioni didattiche necessarie al motore: anno tipico per materia, stati delle competenze, finestra di evidence events, objective stack, sessioni recenti, fingerprint e preferenze operative.

## Capability boundary

Curriculum coverage e generation coverage sono distinte. TutorLab puo conoscere un nodo curricolare senza avere ancora una task family capace di generare una sessione di qualita per quel nodo. In quel caso il dispatcher restituisce `needs_review` con `task_family_not_available:<competency_id>`.

Il motore non deve inventare copertura.

## Composizione

- `path_selector.py` individua root target e working target.
- `stack_bridge.py` inizializza o riprende l'objective stack.
- `decision_bridge.py` applica l'Adaptive Engine.
- `plan_kernel.py` traduce la decisione in una transizione didattica.
- `session_dispatch.py` genera la sessione solo se la capability esiste.
- `result_transition.py` trasforma il risultato in evidenze e next step.
- `learning_snapshot.py` aggiorna snapshot, evidenze e storico recente.

Questi moduli sono volutamente funzionali e indipendenti da database, API web e UI.
