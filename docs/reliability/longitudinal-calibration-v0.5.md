# Longitudinal Simulation Lab + Mastery Calibration v0.5

## Scopo

Questo blocco stressa il motore adattivo su traiettorie sintetiche di più sessioni e usa i risultati per calibrare la gestione di padronanza, prerequisiti, contraddizione e quantità minima di evidenza.

Le simulazioni sono test ingegneristici. Non costituiscono una validazione psicometrica né una prova di efficacia didattica su studenti reali.

## Problemi individuati nella baseline

Le prove longitudinali hanno evidenziato quattro rischi architetturali:

1. una sequenza normale di apprendimento con errori iniziali e successi successivi poteva essere interpretata troppo facilmente come evidenza contraddittoria;
2. un prerequisito recuperato doveva soddisfare gli stessi criteri severi usati per avanzare nel curriculum, con rischio di permanenza eccessiva nel recupero;
3. vecchie ipotesi di errore potevano continuare a influenzare il routing anche dopo successi autonomi successivi;
4. una sola quantità minima di evidenze non rappresentava bene famiglie diverse, per esempio calcolo procedurale e produzione comunicativa in inglese.

## Calibrazione v0.2 della policy

La policy mantiene prudenti le soglie globali di `advance` e `extend`, ma introduce:

- `recovery_exit`: criterio più mirato per considerare sufficientemente riparato un prerequisito;
- `post_recovery_reassess`: rivalutazione obbligatoria dell'obiettivo sospeso dopo l'uscita dal recupero;
- `contradiction_window` e soglia configurabile per distinguere alternanza recente da semplice progresso storico;
- `hypothesis_clean_success_decay`: riduzione del peso delle ipotesi di errore quando compaiono evidenze successive pulite;
- rubriche di sufficienza dell'evidenza per famiglie disciplinari.

## Rubriche per famiglie

Le rubriche non assegnano voti e non sostituiscono le dimensioni di mastery. Specificano quanta evidenza indipendente e di transfer è necessaria prima che una decisione di advance/extend possa essere considerata sufficientemente supportata.

Le famiglie iniziali distinguono:

- matematica procedurale;
- matematica simbolica;
- matematica concettuale/geometrica;
- matematica di ragionamento, dati e pratiche;
- sistema linguistico inglese;
- abilità ricettive inglesi;
- abilità comunicative/produttive e mediazione;
- strategie e interculturalità.

## Profili sintetici

Il laboratorio comprende dodici profili distribuiti tra Matematica e Inglese: forti, tipici, con prerequisito fragile, dipendenti dallo scaffolding, intermittenti e con difficoltà concettuali/strategiche.

Ogni traiettoria produce eventi sintetici con esito, livello di supporto, transfer, qualità della spiegazione ed eventuali osservazioni d'errore. Le abilità latenti sono note al simulatore e fungono da oracolo ingegneristico per individuare routing chiaramente prematuri o recuperi mancati.

## Metriche

Le metriche principali sono:

- avanzamenti prematuri;
- falsi recuperi;
- loop di reassessment;
- tasso di individuazione dei prerequisiti mancanti;
- tasso di ritorno dal recupero all'obiettivo sospeso;
- capacità dei profili forti di avanzare;
- capacità del motore di non promuovere troppo presto profili che riescono solo con forte supporto.

## Validazione senza costi GitHub Actions

TutorLab non usa più workflow GitHub per questi controlli. Gli script restano versionati, ma vengono eseguiti localmente o manualmente:

```bash
python3 tools/run_longitudinal_simulations.py
python3 tools/calibrate_mastery.py
python3 tools/run_local_validation.py
```

`run_longitudinal_simulations.py` applica criteri di accettazione fissi. `calibrate_mastery.py` confronta configurazioni candidate con una funzione di costo conservativa e non modifica mai automaticamente la configurazione. `run_local_validation.py` raccoglie anche tutte le verifiche pregresse di TutorLab.

## Principio di sicurezza didattica

La calibrazione privilegia il costo dell'avanzamento prematuro rispetto alla semplice velocità di progressione. Una policy migliore non è quella che fa avanzare più rapidamente, ma quella che usa evidenze sufficienti, recupera quando necessario, ritorna all'obiettivo iniziale e riconosce l'incertezza quando le evidenze non bastano.
