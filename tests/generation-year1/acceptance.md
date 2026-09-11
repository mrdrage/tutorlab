# Generation Coverage v0.2 — acceptance criteria

Il macro-blocco è accettabile solo se tutti i nodi curricolari di 1ª media per Matematica e Inglese sono eseguibili dal Session Engine.

## Criteri strutturali

- ogni nodo di `year-1.json` compare nella registry delle task family;
- per ogni nodo si costruiscono senza eccezioni una sessione `advance` e una `reassess`;
- entrambe superano il quality gate del Session Engine;
- ogni task possiede prompt, modalità di risposta, banda, supporto, soluzione lato tutor, rubrica, dimensioni osservate, fingerprint e competency id;
- la student view non espone soluzioni, rubriche, parametri generativi o error signals.

## Criteri pedagogici

- `reassess` misura senza insegnamento preventivo;
- `advance` include pratica indipendente e transfer;
- la difficoltà cambia per richiesta cognitiva, autonomia o trasferimento, non per semplice aumento di quantità;
- gli esercizi chiusi hanno una risposta determinabile;
- produzioni orali/scritte, interazione, mediazione e altre risposte aperte usano rubrica e scoring esterno;
- listening conserva lo script nel lato tutor e non lo rende visibile nella student view;
- ogni task resta ancorato alla competenza curricolare dichiarata.

## Copertura disciplinare attesa

Matematica deve includere numeri, pratiche matematiche, geometria e dati. Inglese deve includere grammatica, lessico, fonologia, reading, listening, interaction, spoken production, writing, mediation, strategie e consapevolezza interculturale.

La CI è la fonte di verità sulla copertura effettiva: se viene aggiunto un nuovo nodo a un curriculum di 1ª media senza una family generativa, il controllo deve fallire.
