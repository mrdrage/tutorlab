# Language Expansion v0.6 — acceptance criteria

Il macro-blocco è accettabile solo se tutti i controlli vengono eseguiti localmente/manualmente, senza GitHub Actions.

## Curriculum

- Italiano contiene 45 nodi complessivi nei tre anni.
- Francese contiene 46 nodi complessivi e usa A1 come traguardo finale QCER.
- Spagnolo contiene 46 nodi complessivi e usa A1 come traguardo finale QCER.
- Gli ID sono univoci e usano i prefissi `ita.`, `fr.`, `es.`.
- Ogni prerequisito punta a un nodo esistente della stessa disciplina.
- Non sono ammessi cicli intenzionali di prerequisiti.
- `typical_year` è sequenziamento TutorLab e non viene presentato come prescrizione ministeriale.

## Language Core

- Italiano conserva un modello disciplinare proprio.
- Francese e Spagnolo condividono modalità e infrastruttura, ma non grafi grammaticali.
- Reception, production, interaction e mediation restano distinguibili.
- Grammatica, lessico e fonologia sono risorse, non proxy della competenza comunicativa complessiva.
- Listening conserva lo script nella tutor view e non nella student view.
- Produzioni aperte hanno rubrica e non ricevono scoring automatico inventato.

## Generation coverage

Per ciascuno dei 137 nuovi nodi il Session Engine deve costruire senza errori:

- `recover`
- `consolidate`
- `advance`
- `extend`
- `reassess`

Totale minimo: **685 varianti adattive**.

Ogni sessione deve superare il quality gate, produrre almeno un task quando previsto e non esporre nella student view `solution`, `rubric`, `error_signals` o `generation_parameters`.

## Integrazione

- `curriculum_access` riconosce `ita.`, `fr.`, `es.`.
- `path_selector` supporta Italiano, Francese e Spagnolo.
- La registry generativa include tutti i nuovi nodi.
- Le mastery rubric distinguono sistema linguistico, ricezione, comunicazione e strategie.
- `tools/run_local_validation.py` richiama `tools/check_language_expansion.py`.
- `.github/workflows` deve restare assente.
