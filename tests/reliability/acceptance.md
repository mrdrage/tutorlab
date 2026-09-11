# Reliability & mastery calibration v0.5 — acceptance criteria

Questo macro-blocco usa esclusivamente profili e risultati sintetici. Serve a verificare la coerenza ingegneristica del motore adattivo; non misura efficacia didattica reale e non sostituisce una futura validazione con tutor e studenti.

## Banco prova longitudinale

La suite comprende profili forti, tipici, con prerequisito mancante, dipendenti dal supporto, intermittenti e con difficoltà concettuali o strategiche, in Matematica e Inglese.

Il runner standard esegue 50 semi per 12 profili, 12 sessioni per traiettoria: 600 traiettorie sintetiche e fino a 7.200 sessioni simulate.

## Criteri minimi

- avanzamenti prematuri medi <= 0,02 per traiettoria;
- falsi recuperi medi <= 0,05 per traiettoria;
- loop di reassessment medi <= 0,02 per traiettoria;
- almeno il 90% dei gap di prerequisito deve essere individuato entro le prime cinque decisioni;
- almeno il 90% dei percorsi di recupero deve riuscire a tornare all'obiettivo sospeso;
- almeno il 95% dei profili forti deve ricevere advance/extend entro cinque decisioni;
- almeno il 95% dei profili dipendenti dal supporto non deve ricevere advance/extend nelle prime otto decisioni.

## Regole di calibrazione

1. Le soglie globali di advance/extend non vengono abbassate solo per aumentare la velocità di progressione.
2. Il recupero usa un criterio di uscita distinto dalla padronanza piena del nodo curricolare.
3. Dopo un recupero riuscito l'obiettivo sospeso viene rivalutato prima di proseguire.
4. Errori storici perdono forza quando sono seguiti da evidenze pulite, autonome e coerenti.
5. La contraddizione richiede alternanza recente non spiegata, non semplice presenza storica di successi e insuccessi.
6. Le famiglie disciplinari possono richiedere quantità diverse di evidenze autonome e di transfer.
7. Il tool di calibrazione confronta configurazioni candidate ma non modifica automaticamente la policy.

## Esecuzione locale

I controlli sono manuali/locali e non usano GitHub Actions:

```bash
python3 tools/run_longitudinal_simulations.py
python3 tools/calibrate_mastery.py
python3 tools/run_local_validation.py
```

Un cambiamento alla policy è accettabile solo se mantiene i criteri sopra e non rompe le validazioni pregresse del curriculum, Session Engine, Learning Snapshot e generation coverage.
