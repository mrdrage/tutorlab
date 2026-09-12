# Upper Secondary Architecture v0.7 — grafo curricolare

## Modello di composizione

Il curriculum delle superiori non viene duplicato per ogni indirizzo. TutorLab compone più layer:

1. `common_core`: competenze comuni al livello o a più famiglie di percorso;
2. `family_core`: competenze proprie di licei, tecnici o professionali;
3. `indirizzo`: overlay specifico dell'indirizzo;
4. `articolazione`: overlay scelto tipicamente in una fase successiva;
5. `opzione`: variante ancora più specifica;
6. `profile`: eccezioni o profili puntuali versionati.

Un profilo attivo risolve l'insieme dei layer applicabili e produce il grafo effettivo.

## Esempio concettuale

Per uno studente di un tecnico Informatica:

`common_core`
→ `family_core: tecnico`
→ `indirizzo: Informatica e Telecomunicazioni`
→ `articolazione: Informatica`

Per un liceo scientifico scienze applicate:

`common_core`
→ `family_core: liceo`
→ `indirizzo: Liceo scientifico`
→ `opzione: Scienze applicate`

Questo evita di mantenere copie quasi identiche di algebra, reading o writing in molti percorsi.

## Prerequisiti verticali

Un nodo superiore può avere prerequisiti:

- nello stesso anno;
- in anni precedenti delle superiori;
- direttamente nella scuola media.

Esempio:

`math.numbers.signed-operations`
→ `math.relations.algebraic-expressions`
→ `math.us.foundation.algebra-control`
→ futuri nodi di algebra e funzioni del biennio.

Il recupero può quindi attraversare il confine tra cicli senza creare un secondo motore adattivo.

## Stage year e difficoltà

`stage_year` non è difficulty band.

Un task di prima superiore può essere Band 4 se richiede transfer o scelta strategica, mentre un recupero di quarta superiore può usare un nodo delle medie a Band 1-2. Il Difficulty Engine resta indipendente dalla collocazione curricolare.

## Regola per i quadriennali

`stage_year` descrive la posizione dentro il percorso frequentato; `duration_years` appartiene al profilo. Il motore non assume che una competenza del quinto anno esista in un percorso quadriennale. La futura risoluzione dei curriculum dovrà rifiutare layer o nodi incompatibili con `duration_years`.

## Versionamento

Ogni grafo dichiara:

- `curriculum_profile`;
- validità temporale;
- layer;
- fonti nel relativo documento di profilo.

Questo è necessario soprattutto durante transizioni normative, come la revisione dell'istruzione tecnica avviata dalle classi prime 2026/27.

## Capability boundary

v0.7 rende il motore capace di **rappresentare e risolvere** il contesto delle superiori. Non dichiara ancora completa la generation coverage 1ª-5ª.

Fino alla v0.8:

- i nodi gateway architetturali possono essere usati nei test di composizione;
- i curriculum completi Math/English delle superiori restano `needs_review` se non ancora presenti nella registry generativa.

Questa distinzione impedisce a TutorLab di fingere copertura solo perché conosce la struttura scolastica.
