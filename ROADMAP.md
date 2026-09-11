# TutorLab Roadmap

## Stato dei macro-blocchi

- [x] **Fondazioni pedagogiche + Difficulty Engine v0.1**
- [x] **Curriculum Matematica 1ª-3ª media + grafo dei prerequisiti v0.1**
- [x] **Curriculum Inglese 1ª-3ª media + progressione A1-A2**
- [ ] **Motore adattivo: diagnosi, errori e decisione del passo successivo**
- [ ] **Generazione di sessioni didattiche complete e criteri di qualità**
- [ ] **Profili studente e contratto futuro con Hub Scuola**

I macro-blocchi sono l'unità di avanzamento del progetto. Le attività interne possono essere granulari, ma un blocco viene considerato completato solo quando produce un sottosistema coerente, documentato e verificabile.

## v0.1 — Fondazioni

Obiettivo: dimostrare che TutorLab possiede un metodo didattico coerente e rappresentabile in dati strutturati.

Deliverable:

- manifesto e visione;
- pedagogia comune;
- tassonomia degli errori;
- schema formale di una competenza;
- modello dei livelli di difficoltà;
- curriculum iniziale 1ª-3ª media per Matematica;
- curriculum iniziale 1ª-3ª media per Inglese;
- un vertical slice completo di Matematica;
- un vertical slice completo di Inglese;
- formato delle sessioni e dei risultati;
- criteri di recupero, consolidamento, avanzamento e potenziamento;
- esempi con studenti fittizi;
- test qualitativi sulla generazione.

Non-obiettivi:

- UI completa;
- database di studenti;
- integrazione diretta con Hub Scuola;
- login/account;
- generazione massiva di PDF;
- riproduzione di manuali protetti da copyright.

## v0.2 — Curriculum e prerequisiti

- completare il grafo delle competenze di matematica;
- completare il grafo delle competenze di inglese;
- introdurre fonti curricolari versionate e data di revisione;
- formalizzare relazioni tra prerequisito, obiettivo e competenze successive;
- introdurre rubriche di padronanza per famiglie di competenze.

## v0.3 — Generazione controllata

- definire famiglie di esercizi parametrizzate;
- separare contenuto, difficoltà e grado di guida;
- introdurre vincoli anti-ripetizione;
- generare esempi, pratica, verifica e recupero dallo stesso nodo di competenza;
- testare coerenza delle soluzioni e appropriatezza per classe.

## v0.4 — Adattamento

- modello di sessione;
- modello di risultato;
- storico sintetico delle evidenze;
- decision engine iniziale;
- scelta tra recover, consolidate, advance, extend e reassess;
- simulazioni con profili fittizi longitudinali.

## v0.5 — Nuove materie

Portare il framework comune su almeno due discipline non isomorfe alla matematica:

- Italiano;
- una tra Scienze, Storia o Geografia.

Obiettivo: verificare che l'architettura sia realmente multidisciplinare.

## v0.6 — Esperienza Tutor

- comandi ad alto livello, es. «preparami 40 minuti»;
- output pronto per lezione;
- modalità diagnosi, recupero, verifica e ripasso;
- controllo esplicito di tempo, difficoltà e quantità;
- esportazione strutturata delle evidenze.

## v0.7 — Integrazione Hub Scuola

- contratto dati stabile tra Hub Scuola e TutorLab;
- importazione di un profilo didattico pseudonimizzato/locale;
- restituzione di attività, evidenze e prossimo obiettivo;
- nessuna dipendenza di TutorLab dalla UI di Hub Scuola.

## v1.0 — TutorLab stabile

TutorLab 1.0 deve poter:

1. ricevere un profilo didattico;
2. scegliere un obiettivo coerente;
3. verificare prerequisiti;
4. costruire una sessione completa;
5. interpretare i risultati;
6. proporre il passo successivo;
7. motivare la propria decisione didattica in modo verificabile dal tutor.
