# Upper Secondary Architecture v0.7 — modello dati

## Principio

TutorLab separa tre concetti che non devono essere confusi:

1. **Academic context**: dove si trova lo studente (`school_stage`, anno, anno scolastico, profilo frequentato).
2. **Education pathway**: struttura istituzionale del percorso (liceo/tecnico/professionale, indirizzo, articolazione, opzione, durata, variante).
3. **Curriculum graph**: competenze e prerequisiti effettivamente applicabili a quel contesto.

Il livello scolastico o l'indirizzo non sono proprietà della competenza dello studente. Sono contesto curricolare.

## Perché il percorso è un oggetto versionato

La secondaria di secondo grado italiana non è un unico percorso. Esistono licei, istituti tecnici e professionali, con indirizzi, articolazioni e opzioni. Inoltre il quadro può cambiare nel tempo: per esempio l'istruzione tecnica entra in una fase di riforma dalle classi prime 2026/27 e il sistema include anche percorsi quadriennali della filiera tecnologico-professionale.

Per questo un profilo contiene almeno:

- `family`: liceo / tecnico / professionale;
- `duration_years`: 4 o 5;
- `pathway_variant`: standard, quadriennale di filiera o altra sperimentazione;
- `sector`, quando esiste;
- `indirizzo`;
- `articolazione`, `opzione`, `specializzazione`, quando pertinenti;
- `selection_year`, per rappresentare scelte che avvengono dopo il primo anno;
- validità temporale e `status`;
- fonti normative tramite `source_refs`.

Il catalogo `curriculum/upper-secondary/pathways/catalog.seed.json` è volutamente un seed architetturale: copre le forme strutturali che il motore deve saper rappresentare, non pretende di essere il catalogo esaustivo di ogni singola opzione autorizzata sul territorio.

## Academic context

Lo schema `academic-context.schema.json` mantiene la compatibilità con le medie e aggiunge il contesto delle superiori.

Esempio:

```json
{
  "school_stage": "upper_secondary",
  "stage_year": 3,
  "school_year": "2028/29",
  "pathway_profile_id": "it.upper.tecnico-informatica",
  "pathway_variant": "standard",
  "curriculum_profile_ids": [
    "it-upper-common-2026",
    "it-upper-tecnico-tech-2026",
    "it-upper-informatica-2026"
  ]
}
```

## Compatibilità con Learning Snapshot

Il Learning Snapshot continuerà a conservare padronanza, evidenze, errori e objective stack per materia. Il contesto accademico viene aggiunto separatamente e non modifica retroattivamente gli stati di competenza.

Una competenza non diventa più o meno padroneggiata perché lo studente cambia indirizzo. Cambia invece il sottoinsieme di nodi curricolari applicabili e il prossimo obiettivo possibile.

## Identità dei nodi superiori

I nuovi nodi della secondaria di secondo grado usano il namespace:

- `math.us.*`
- `eng.us.*`
- in futuro `<subject>.us.*`

I nodi delle medie restano invariati. Un prerequisito di un nodo `math.us.*` può quindi puntare direttamente a un nodo `math.*` della scuola media, rendendo esplicito il ponte verticale.

## Regola di sicurezza architetturale

TutorLab non deve dedurre il programma solo da `stage_year`. La coppia minima per risolvere un curriculum delle superiori è:

`school_stage + stage_year + pathway_profile_id + curriculum profile version`

Se il profilo non è noto o non è compatibile con l'anno scolastico richiesto, il sistema deve richiedere revisione invece di inventare un percorso.
