# Generation Coverage 2ª media v0.3

## Obiettivo

Rendere eseguibili dal Session Engine tutti i nodi curricolari di seconda media per Matematica e Inglese senza indebolire quality gate, separazione student/tutor view, anti-ripetizione e capability boundary.

## Copertura verificata

La CI confronta direttamente la registry con i due file curricolari `year-2.json` e costruisce per ogni nodo le cinque modalità adattive:

- `recover`
- `consolidate`
- `advance`
- `extend`
- `reassess`

Risultato della prima validazione completa:

- Matematica: 21 nodi eseguibili
- Inglese: 32 nodi eseguibili
- Totale: 53 nodi
- Varianti di sessione esercitate: 265

## Matematica

La copertura include pratiche matematiche, numeri, geometria, relazioni e dati. I task non si limitano al calcolo: includono scelta della strategia, interpretazione, modellizzazione, argomentazione, cambio di rappresentazione e transfer.

Particolare attenzione è data ai gateway tipici della seconda media: rapporti, proporzioni, percentuali, radice quadrata, area, Pitagora, similitudine e proporzionalità.

## Inglese

La copertura segue il ponte A1→A2 e mantiene la distinzione fra strumenti linguistici e competenze d'uso. Sono coperte grammatica, lessico, fonologia, reading, listening, spoken interaction, spoken production, writing, mediation, learning strategies e interculturalità.

Le produzioni aperte usano rubriche e scoring esterno. I task di listening conservano lo script nella tutor view e non lo espongono nella student view.

## Regola di copertura

Un nodo non è considerato eseguibile solo perché presente nella registry. Deve:

1. generare una sessione valida in tutte le modalità adattive;
2. superare `validate_session`;
3. produrre task con campi minimi, rubrica e soluzione/target di scoring;
4. non esporre solution, rubric, generation parameters o error signals nella student view;
5. restare compatibile con Learning Snapshot, Session Engine e CI curricolare esistenti.

## Capability boundary

Dopo la copertura completa di seconda media, il test del confine di capacità usa un nodo reale di terza media (`math.numbers.signed-number-sense`). Finché quel nodo non avrà una famiglia generativa, TutorLab deve restituire `needs_review` invece di improvvisare.
