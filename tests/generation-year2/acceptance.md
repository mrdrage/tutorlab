# Acceptance — Generation Coverage 2ª media

Il macro-blocco è accettato solo se valgono contemporaneamente i criteri seguenti.

1. Ogni nodo dei curriculum di Matematica e Inglese `year-2.json` è registrato nel Session Engine.
2. Per ogni nodo vengono costruite senza errore sessioni `recover`, `consolidate`, `advance`, `extend` e `reassess`.
3. Ogni sessione supera il quality gate comune.
4. La student view non espone soluzioni, rubriche, parametri generativi o segnali diagnostici.
5. I task aperti hanno una rubrica/target di scoring esplicito e non simulano una valutazione deterministica non disponibile.
6. I task di listening mantengono il materiale sorgente lato tutor.
7. La matematica include evidenze di ragionamento/strategia oltre al mero risultato numerico nei task di transfer.
8. Le competenze linguistiche comunicative non sono ridotte alla sola accuratezza grammaticale.
9. La copertura di seconda media non rompe la copertura completa di prima media.
10. Learning Snapshot, Session Engine e validazione curricolare preesistenti restano verdi.
11. Un nodo di terza media non ancora coperto continua a produrre `needs_review`, preservando la capability boundary.

La CI `Year-2 generation coverage` verifica automaticamente i punti strutturali e genera 5 varianti adattive per ogni nodo curricolare di seconda media.