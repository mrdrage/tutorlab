# TutorLab

TutorLab è un motore didattico adattivo per tutor e studenti.

L'obiettivo è costruire una **collana didattica viva e generativa**: non una raccolta statica di esercizi, ma un sistema capace di capire cosa uno studente sa, individuare prerequisiti mancanti, proporre attività calibrate, interpretare gli errori e decidere il passo didattico successivo.

La prima fase è dedicata alla **scuola secondaria di primo grado (1ª, 2ª e 3ª media)**, con moduli iniziali di **Matematica** e **Inglese**. L'architettura è pensata per estendersi a Italiano, Francese, Scienze, Storia e Geografia.

## Ciclo didattico

TutorLab segue un ciclo comune:

1. diagnosi;
2. verifica dei prerequisiti;
3. spiegazione essenziale;
4. esempio svolto;
5. esercizio guidato;
6. pratica autonoma;
7. verifica;
8. analisi dell'errore;
9. recupero, consolidamento o potenziamento;
10. nuova verifica.

Il principio guida è semplice: **TutorLab deve sapere cosa insegnare dopo, non soltanto generare contenuti.**

## Stato

Il progetto è in fase di fondazione. Il primo target è **TutorLab v0.1**.

La v0.1 formalizzerà:

- principi pedagogici;
- schema delle competenze;
- tassonomia degli errori;
- livelli di difficoltà;
- curriculum 1ª-3ª media per Matematica e Inglese;
- formato delle sessioni didattiche e dei risultati;
- criteri di avanzamento, recupero e consolidamento;
- primi percorsi completi end-to-end.

## Relazione con Hub Scuola

TutorLab nasce come progetto indipendente.

- **TutorLab**: motore didattico e decisionale.
- **Hub Scuola**: gestione, memoria e visualizzazione del percorso dello studente.

Una futura integrazione permetterà a Hub Scuola di fornire il profilo didattico dello studente e a TutorLab di restituire attività, analisi degli errori e prossimo obiettivo consigliato.

## Privacy

Nessun dato reale degli studenti deve essere versionato nel repository. Esempi, test e fixture devono usare soltanto identità fittizie.

## Licenza e contenuti

TutorLab produrrà materiale didattico originale. Non ha l'obiettivo di riprodurre testi o esercizi di manuali scolastici protetti da copyright.
