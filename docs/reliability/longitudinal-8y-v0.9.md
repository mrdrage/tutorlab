# Longitudinal Reliability v0.9

## Obiettivo

Verificare che TutorLab resti coerente su una traiettoria verticale di otto checkpoint, dalla 1ª media alla 5ª superiore, senza trasformare gli errori vecchi in una condanna permanente e senza accelerare artificialmente gli avanzamenti.

La simulazione è un banco prova ingegneristico sintetico. Non è una validazione psicometrica o sperimentale su studenti reali.

## Traiettorie

Sono presenti otto profili: forte, tipico, gap cross-stage e dipendenza dal supporto, per Matematica e Inglese.

Ogni percorso attraversa otto target consecutivi. I profili cross-stage incontrano in prima superiore un prerequisito fragile proveniente dalle medie e possono scendere a una seconda lacuna annidata. Lo stack deve poi risalire in ordine e rivalutare l'obiettivo sospeso.

## Problema emerso

Con la mastery calcolata su tutte le evidenze storiche, un recupero poteva riuscire ma le prime prove fallite continuavano a pesare indefinitamente. Il motore riconosceva e risolveva la lacuna, tornava al target, ma restava eccessivamente inerziale.

Non era opportuno risolvere il problema abbassando le soglie di advance: questo avrebbe aumentato il rischio di avanzamenti prematuri in tutto il sistema.

## Calibrazione scelta

La policy v0.3 introduce `mastery_evidence_window = 12`.

- gli evidence event grezzi continuano a essere conservati nello storico;
- lo stato corrente di mastery usa le 12 evidenze più recenti della competenza;
- il summary espone sia `lifetime_event_count` sia `active_window_event_count`;
- errori vecchi non rappresentativi possono uscire dalla finestra corrente senza essere cancellati dalla storia.

Il confronto sintetico su finestre 0, 12, 18 e 24 ha favorito 12. Con 40 seed il costo comparativo osservato è stato:

- window 12: 10.625;
- window 18: 26.25;
- window 24: 35.625;
- nessuna finestra: 69.75.

La funzione di costo penalizza in modo prioritario avanzamenti prematuri, falsi recuperi, mancato ritorno dal recupero e stagnazione. Il calibratore non modifica automaticamente la policy.

## Risultato del banco prova esteso

Nel controllo equivalente su 100 seed per profilo e massimo 16 sessioni sintetiche per checkpoint:

- premature advance per run: 0.00875;
- false recovery per run: 0.005;
- reassessment loop per run: 0.00375;
- strong complete 8-year rate: 1.00;
- typical complete 8-year rate: 1.00;
- cross-stage gap complete 8-year rate: 0.915;
- cross-stage recovery detect rate: 1.00;
- cross-stage return rate: 1.00;
- deep recovery detect rate: 0.93;
- deep recovery return rate: 0.93;
- support dependency guard rate: 1.00.

## Regressione v0.5

La stessa finestra è stata verificata contro la suite Reliability v0.5. Nel banco prova equivalente restano soddisfatti i criteri precedenti: nessun avanzamento prematuro sistematico, recovery detection circa 99%, recovery return 100%, strong progress 100% e support-dependency guard 100%.

## Limiti

Le percentuali dipendono dal modello sintetico e dai seed fissati. Servono a confrontare versioni del motore, non a stimare il comportamento di studenti reali. Prima di interpretare queste soglie come evidenza educativa esterna saranno necessari dati reali, consenso e un protocollo di valutazione separato.

## Esecuzione

- `python3 tools/run_longitudinal_8y.py`
- `python3 tools/calibrate_longitudinal_8y.py`
- `python3 tools/check_mastery_evidence_window.py`
- `python3 tools/run_local_validation.py`

Nessun GitHub Actions workflow viene utilizzato.
