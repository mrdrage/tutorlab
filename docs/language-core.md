# TutorLab Language Core v0.6

TutorLab usa un nucleo linguistico comune per le competenze che condividono una struttura didattica, senza rendere identiche discipline diverse.

## Principio architetturale

Il Language Core descrive modalità e comportamenti comuni:

- ricezione: reading/listening o comprensione di testi orali e scritti;
- produzione: oralità, spoken production e writing;
- interazione;
- mediazione;
- sistema linguistico: grammatica, lessico, fonologia/ortografia;
- strategie di apprendimento, riparazione e revisione;
- dimensione interculturale/plurilingue.

Francese e Spagnolo usano direttamente questa architettura come seconde lingue comunitarie. Italiano usa soltanto i meccanismi comuni utili, mantenendo un modello disciplinare proprio: oralità, lettura, scrittura, grammatica, lessico, analisi testuale e strategie di studio.

## Traguardi

- Inglese: A2 al termine della secondaria di primo grado.
- Francese e Spagnolo come seconda lingua comunitaria: A1 al termine della secondaria di primo grado.
- Italiano: nessun livello CEFR; la progressione è definita dalle competenze disciplinari nazionali e dalla sequenza interna TutorLab.

I livelli CEFR non sostituiscono il curriculum: descrivono la capacità d'uso della lingua. Le strutture grammaticali e il lessico sono risorse al servizio dei compiti comunicativi.

## Relazioni

Le lingue straniere possono condividere famiglie di task e rubriche, ma non condividono automaticamente prerequisiti grammaticali: ogni lingua conserva il proprio grafo.

Le competenze plurilingui possono usare confronti tra lingue come strategia, ma TutorLab evita di assumere equivalenze perfette tra strutture o significati.

## Generation layer

`engine/language_core.py` costruisce task originali a partire dal nodo curricolare e dalla fase didattica. Il layer distingue:

- language-resource task per grammatica, lessico e fonologia;
- reading task con testo originale;
- listening task con script disponibile solo nella tutor view;
- productive/open task per interazione, produzione, scrittura, mediazione, analisi e strategie.

Le produzioni aperte restano valutate tramite rubrica. Il motore non inventa un punteggio automatico quando non dispone di evidenza sufficiente.
