# Math + English Upper Secondary v0.8 — acceptance criteria

Il macro-blocco non è completo perché i file curricolari esistono. È completo soltanto quando curriculum, resolver, generazione e ciclo adattivo concordano.

## Curriculum e struttura

- Matematica e Inglese devono coprire gli anni 1-5 attraverso `common_core` + overlay di percorso, senza clonare il common core per ogni indirizzo.
- Ogni ID deve essere unico nell'intero stage superiore della materia.
- Ogni prerequisito deve risolversi in un nodo esistente delle medie o delle superiori.
- I nodi superiori usano namespace `math.us.*` o `eng.us.*`.
- Gli overlay liceali, tecnici e professionali devono apparire solo nei profili applicabili.
- Scientifico/scienze applicate può aggiungere profondità senza rendere obbligatoria la stessa profondità in ogni liceo.
- I percorsi quadriennali non devono ricevere automaticamente un quinto anno.
- La validità temporale del grafo e del profilo deve essere rispettata.

## Inglese

- Ogni `eng.us.*` dichiara `cefr_anchor` e `progression_stage`.
- `B1_plus` è una fascia interna TutorLab, non un nuovo livello QCER.
- Reading, Listening, Spoken Interaction, Spoken Production, Writing e Mediation restano distinguibili.
- Grammatica e lessico sono risorse della competenza comunicativa, non sinonimi di padronanza della lingua.
- Licei e tecnici arrivano a un target B2 integrato.
- Il professionale sviluppa gradualmente linguaggio generale + settoriale e arriva a un target didattico B2; eventuali soglie INVALSI diverse sono trattate come reporting di assessment, non come tetto curricolare.
- I listening conservano lo script nella tutor view e non lo espongono nella student view.
- Le produzioni aperte richiedono rubrica/scoring esterno quando non sono deterministiche.

## Matematica

- La difficoltà non viene aumentata soltanto usando numeri più grandi.
- Le famiglie devono distinguere almeno algebra/equazioni, funzioni, geometria, trigonometria, probabilità/statistica, esponenziali/logaritmi e analisi quando applicabile al profilo.
- I worked example mostrano realmente un modello o una soluzione da analizzare.
- I task di transfer richiedono scelta, spiegazione, modellizzazione o cambio di rappresentazione quando pertinente.
- Un errore in un nodo superiore può attivare recupero su un prerequisito delle medie senza perdere il root target.

## Generation coverage

Per ogni nodo superiore risolto da almeno un profilo seed:

- `load_competency(id)` deve riuscire;
- `can_generate(id)` deve essere vero;
- la mastery rubric non deve ricadere nel fallback generico;
- devono essere costruibili `recover`, `consolidate`, `advance`, `extend`, `reassess`;
- ogni sessione deve superare `session_quality.validate_session`;
- student view e tutor view devono restare separate;
- la registry non deve coprire ID inventati fuori curriculum.

## Qualità generativa

- Almeno un campione per ogni strand deve essere testato su più seed.
- I prompt di transfer devono mostrare diversità semantica, non solo fingerprint diversi.
- Worked example e targeted model devono essere riconoscibili come modelli.
- I task aperti devono avere rubriche.
- Gli strand professionali e interculturali di Inglese usano generatori dedicati, non un fallback vuoto.

## Vertical slice

Devono passare almeno:

1. **Matematica scientifico, quinto anno**: nodo avanzato → sessione → risultato → evidence events → competency state → next step.
2. **Inglese liceale B2, quinto anno**: nodo integrato → sessione → risultato → evidence events → competency state → next step.
3. Recupero cross-stage superiore → prerequisito delle medie → ritorno/rivalutazione del target sospeso.

## Regressione

Devono restare validi:

- curriculum e generation coverage Math/English 1ª-3ª media;
- Language Expansion Italiano/Francese/Spagnolo;
- Adaptive Engine;
- Session Engine;
- Learning Snapshot legacy 0.1;
- Learning Snapshot 0.2 e resolver upper-secondary;
- Reliability/mastery calibration già esistenti.

## Costi e validazione

- `.github/workflows` deve restare assente.
- Nessun test viene delegato a GitHub Actions.
- I test v0.8 sono inclusi in `tools/run_local_validation.py` e sono eseguiti localmente/manuali.
- Se l'ambiente non permette il checkout completo del repository, non si dichiara falsamente il runner completo come superato: si eseguono test equivalenti sui confini modificati e si documenta la limitazione prima del merge.
