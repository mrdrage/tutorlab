# TutorLab

TutorLab è un motore didattico adattivo per tutor e studenti.

L'obiettivo è costruire una **collana didattica viva e generativa**: non una raccolta statica di esercizi, ma un sistema capace di capire cosa uno studente sa, individuare prerequisiti mancanti, proporre attività calibrate, interpretare gli errori e decidere il passo didattico successivo.

Il principio guida è semplice: **TutorLab deve sapere cosa insegnare dopo, non soltanto generare contenuti.**

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

Se emerge una lacuna nei prerequisiti, TutorLab può sospendere temporaneamente l'obiettivo corrente, recuperare la competenza mancante e poi ritornare al target iniziale.

## Stato del progetto

La linea **TutorLab 1.x** consolida il motore come servizio didattico indipendente e integrabile.

La v1.0 comprende:

- curriculum e grafi dei prerequisiti per Matematica e Inglese dalla 1ª media alla 5ª superiore;
- Italiano, Francese e Spagnolo per il triennio della scuola media;
- Adaptive Engine, Session Engine e Learning Snapshot;
- recovery stack e ponti medie -> superiori;
- mastery calibrata su evidenze recenti mantenendo lo storico;
- simulazioni longitudinali fino a otto anni scolastici;
- facade applicativo con intenti `continue / lesson / practice / assessment`;
- Tutor View e Student View separate;
- contratto dati v1.0 per l'integrazione con Hub Scuola.

La v1.1 aggiunge un bridge JSON locale e versionato per invocare il facade TutorLab da processi esterni senza accoppiare il motore a database, UI o autenticazione. Il bridge mantiene separati il versionamento della release TutorLab, del protocollo di trasporto e del contratto Hub Scuola.

Per il dettaglio delle milestone vedere `ROADMAP.md`.

## Relazione con Hub Scuola

TutorLab resta un progetto indipendente.

- **TutorLab**: curriculum, prerequisiti, decisione didattica, generazione delle sessioni e interpretazione dei risultati.
- **Hub Scuola**: identità, persistenza, interfaccia e memoria applicativa dello studente.

L'integrazione avviene tramite contratti versionati: Hub fornisce un Learning Snapshot e una richiesta; TutorLab restituisce sessione, evidenze, aggiornamento dello snapshot e prossimo passo consigliato.

TutorLab non deve conoscere tabelle, account, login o dettagli di storage di Hub Scuola.

## Validazione

Il comando canonico è:

```bash
python tools/run_local_validation.py
```

Le verifiche sono locali/manuali. Il progetto non richiede GitHub Actions o workflow a pagamento.

## Privacy

Nessun dato reale degli studenti deve essere versionato nel repository. Esempi, test e fixture devono usare soltanto identità fittizie.

## Licenza e contenuti

TutorLab produce materiale didattico originale. Non ha l'obiettivo di riprodurre testi o esercizi di manuali scolastici protetti da copyright.
