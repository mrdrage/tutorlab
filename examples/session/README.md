# Session Engine demos

`vertical_slices.py` esegue due circuiti completi senza dati reali di studenti.

## Matematica

Target: `math.numbers.fraction-equivalence`.

La sessione viene generata come `advance`; le risposte sintetiche mostrano un pattern compatibile con prerequisito mancante `math.numbers.fraction-meaning`. Gli evidence events vengono aggregati e l'Adaptive Engine deve proporre `recover` sul prerequisito, conservando l'obiettivo originario per il ritorno successivo.

## Inglese

Target: `eng.grammar.present_simple`.

La sessione viene generata come `consolidate`; le risposte sintetiche mostrano un `procedure_error` ricorrente. Il motore deve preferire `consolidate` sullo stesso target invece di retrocedere arbitrariamente a un prerequisito.

## Esecuzione

Dalla root del repository:

```bash
python3 examples/session/vertical_slices.py
```

L'output contiene `session`, `result`, `state` e `decision` per entrambe le discipline. I dati sono interamente fittizi.
