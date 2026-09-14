# Math + English Upper Secondary v0.8

## Obiettivo

Rendere eseguibile la progressione 1ª-5ª superiore senza introdurre un unico programma artificiale per tutti gli indirizzi.

TutorLab compone:

`common core → family overlay → eventuale profile overlay`

Il curriculum risolto dipende da `academic_context` e dal profilo frequentato.

## Matematica

Il common core costruisce la continuità verticale tra algebra, equazioni/disequazioni, funzioni, geometria, dati/probabilità, trigonometria, esponenziali/logaritmi, successioni e modellizzazione.

Gli overlay regolano la profondità:
- licei: maggiore continuità teorica e analitica;
- scientifico/scienze applicate: ulteriore profondità simbolica, funzionale, probabilistica e di analisi;
- tecnici: modellizzazione, rappresentazioni, dati e applicazioni coerenti con il profilo;
- professionali: matematica funzionale, quantitativa e modellistica legata ai contesti di studio/lavoro.

Le task family generiche sono affiancate da override competency-aware per i nodi che richiedono semantica specifica, ad esempio sistemi, radicali, fattorizzazione, probabilità condizionata, funzioni quadratiche, variabili aleatorie e trasformazioni di grafici.

## Inglese

Progressione interna:

`A2 bridge → B1 developing → B1 core → B1+ interno → B2 developing → B2 target`

`B1+` resta una fascia interna TutorLab e non viene presentata come livello ufficiale QCER.

La generazione distingue:
- grammar/language system;
- vocabulary e linguaggio professionale;
- reading;
- listening;
- spoken interaction;
- spoken production;
- writing;
- mediation;
- learning strategy;
- intercultural competence;
- integrated language use.

Licei e tecnici arrivano a B2 attraverso overlay dedicati. Il professionale costruisce B1+ nel terzo anno, sviluppa B2 nel quarto e usa B2 come target didattico del quinto, con forte integrazione di linguaggi settoriali e mediazione professionale.

## Generation rules

- Ogni nodo superiore presente nel curriculum deve avere una task family registrata.
- `worked_example` deve mostrare un modello reale, non una semplice consegna guidata.
- I task di transfer devono osservare scelta, ragionamento o adattamento a un contesto meno familiare.
- Le produzioni aperte usano rubriche e non ricevono scoring automatico senza evidenza esterna.
- Gli script di listening sono tutor-only.
- I seed devono produrre variazione semantica, non soltanto fingerprint diversi.
- `needs_review` resta riservato a ID realmente fuori dal perimetro implementato.

## Mastery

I nodi `math.us.*` e `eng.us.*` hanno rubriche di sufficienza dedicate e più conservative rispetto al fallback generale. Le soglie sono default ingegneristici; la calibrazione longitudinale completa medie→maturità è rimandata a v0.9.

## Validazione

I test v0.8 sono locali/manuali e coprono:
- schema e prerequisiti;
- composizione per profilo;
- generation coverage completa sulle cinque azioni adattive;
- qualità semantica e diversità;
- allineamento fra competenza e task;
- capability boundary;
- vertical slice Math scientifico e English B2;
- regressioni del ciclo medie;
- assenza di `.github/workflows`.
