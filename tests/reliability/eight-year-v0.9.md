# Longitudinal Reliability 8-year v0.9

## Scopo

Stressare il motore adattivo su traiettorie sintetiche che attraversano otto checkpoint curricolari consecutivi: 1ª-3ª media e 1ª-5ª superiore. Il test non valida TutorLab su studenti reali e non produce soglie psicometriche.

## Profili sintetici

Per Matematica e Inglese vengono simulati quattro comportamenti:

- forte: padronanza alta, transfer stabile, poco rumore;
- tipico: apprendimento progressivo con variabilità moderata;
- gap cross-stage: ingresso alle superiori con un prerequisito fragile delle medie e un secondo prerequisito annidato;
- dipendente dal supporto: buona prestazione con scaffolding ma autonomia insufficiente.

I gap profondi usano lo stack reale del motore fino a profondità 2. Il percorso deve scendere al prerequisito, recuperarlo, risalire al genitore, rivalutarlo e tornare al target superiore sospeso.

## Acceptance criteria

Su 100 seed per profilo e massimo 16 sessioni sintetiche per checkpoint:

- premature advancement <= 0.02 per run;
- false recovery <= 0.02 per run;
- reassessment loop <= 0.02 per run;
- strong complete 8-year rate >= 0.98;
- typical complete 8-year rate >= 0.95;
- cross-stage gap complete 8-year rate >= 0.85;
- cross-stage recovery detect rate >= 0.95;
- cross-stage return rate >= 0.95;
- nested recovery detect rate >= 0.85;
- nested recovery return rate >= 0.85;
- support-dependency guard rate >= 0.98.

## Calibrazione mastery

La simulazione ha evidenziato che una media su tutte le evidenze storiche rendeva il motore eccessivamente inerziale dopo un recupero riuscito. La policy v0.3 usa quindi le ultime 12 evidenze della competenza per stimare la mastery corrente. Lo storico completo degli evidence event resta conservato nel Learning Snapshot.

`tools/calibrate_longitudinal_8y.py` confronta finestre 0, 12, 18 e 24 usando una funzione di costo che penalizza soprattutto avanzamenti prematuri, falsi recuperi, mancato ritorno dal recupero e stagnazione dei profili tipici. Il calibratore è read-only rispetto alla policy: non modifica mai automaticamente la configurazione di produzione.

## Regressioni obbligatorie

La modifica alla finestra di evidenza deve continuare a soddisfare la suite Reliability v0.5. `tools/check_mastery_evidence_window.py` verifica inoltre che:

1. lo storico lifetime non venga eliminato;
2. la finestra attiva contenga esattamente le evidenze recenti configurate;
3. un miglioramento stabile recente possa superare prestazioni vecchie ormai non rappresentative.

## Costi CI

Nessun GitHub Actions workflow. I controlli sono eseguiti tramite `tools/run_local_validation.py` o singolarmente in locale.
