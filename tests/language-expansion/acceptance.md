# Language Expansion v0.6 — acceptance criteria

Il macro-blocco è accettabile solo se tutti i controlli vengono eseguiti localmente/manualmente, senza GitHub Actions.

## Curriculum e fonti

- Italiano contiene 45 nodi complessivi nei tre anni.
- Francese contiene 46 nodi complessivi e usa A1 come traguardo finale QCER.
- Spagnolo contiene 46 nodi complessivi e usa A1 come traguardo finale QCER.
- I nove file curricolari devono risultare validi rispetto allo schema linguistico condiviso.
- Gli ID sono univoci e usano i prefissi `ita.`, `fr.`, `es.`.
- Ogni prerequisito punta a un nodo esistente della stessa disciplina.
- Non sono ammessi cicli intenzionali di prerequisiti.
- `typical_year` è sequenziamento TutorLab e non viene presentato come prescrizione ministeriale.
- Il perimetro disciplinare viene confrontato con le Indicazioni Nazionali 2025 e, per le lingue straniere, con il QCER/CEFR Companion Volume.

## Language Core

- Italiano conserva un modello disciplinare proprio.
- Francese e Spagnolo condividono modalità e infrastruttura, ma non grafi grammaticali.
- Reception, production, interaction e mediation restano distinguibili.
- Grammatica, lessico e fonologia sono risorse, non proxy della competenza comunicativa complessiva.
- I task di grammatica/lessico/fonologia devono includere materiale linguistico concreto, non solo istruzioni generiche.
- Ogni `worked_example` deve esporre un modello esplicito.
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

Il controllo anti-ripetizione deve inoltre conservare headroom generativa: su otto seed rappresentativi ogni competenza deve produrre almeno tre fingerprint distinti in `independent_practice`.

## Pipeline adattiva

Italiano, Francese e Spagnolo devono avere almeno un vertical slice end-to-end che verifichi:

`sessione → risultato valutato → evidence events → competency state → recent activity → next step`

Le risposte esplicitamente valutate non devono restare `pending`; session ID e fingerprint devono entrare nello storico; l'azione successiva deve appartenere al vocabolario adattivo valido.

## Regressione del core esistente

- I generatori Math/English non devono essere modificati dal macro-blocco.
- L'estensione della registry deve essere additiva e i nuovi prefissi non devono collidere con `math.` o `eng.`.
- `curriculum_access` deve continuare a risolvere Matematica e Inglese come prima.
- `path_selector` deve mantenere gating dei prerequisiti e scelta del successore sui soggetti esistenti.
- Le mastery rubric Math/English devono conservare le stesse famiglie e soglie di evidenza della v0.5.
- Le modifiche non devono toccare Adaptive Engine, Session Engine, Learning Snapshot o Reliability logic se non attraverso interfacce già previste.

## Integrazione e costi

- `curriculum_access` riconosce `ita.`, `fr.`, `es.`.
- `path_selector` supporta Italiano, Francese e Spagnolo.
- La registry generativa include tutti i nuovi nodi.
- Le mastery rubric distinguono sistema linguistico, ricezione, comunicazione e strategie.
- Esiste un solo schema curricolare linguistico condiviso, senza duplicazioni concorrenti.
- `tools/run_local_validation.py` richiama `tools/check_language_expansion.py`.
- `.github/workflows` deve restare assente.
