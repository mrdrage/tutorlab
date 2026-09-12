# Upper-secondary pathways

Profilo architetturale di riferimento: a.s. 2026/27.

TutorLab distingue tre famiglie: `liceo`, `tecnico`, `professionale`. Il modello supporta inoltre `sector`, `indirizzo`, `articolazione`, `opzione`, `specializzazione`, `selection_year`, durata e variante del percorso.

Il catalogo seed non è l'elenco territoriale delle scuole. Serve a verificare tutte le forme strutturali necessarie al motore.

Per i licei sono rappresentabili anche opzioni e indirizzi interni, incluso il Liceo del Made in Italy e gli indirizzi del liceo artistico.

Per i tecnici il modello gestisce i due settori, gli indirizzi e le articolazioni. Il profilo 2026/27 è marcato `transition` perché la revisione dell'istruzione tecnica parte dalle classi prime 2026/27, pur mantenendo sostanzialmente la struttura di settori e indirizzi/articolazioni.

Per i professionali il modello conserva gli indirizzi del D.Lgs. 61/2017 e una struttura orientata alle competenze.

I percorsi quadriennali sono rappresentati tramite `duration_years = 4` e `pathway_variant = quadriennale_filiera`; non vengono ottenuti comprimendo automaticamente un percorso quinquennale.

Le fonti ufficiali sono registrate direttamente in `catalog.seed.json` e referenziate dai profili tramite `source_refs`.
