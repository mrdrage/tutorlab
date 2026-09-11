# Fonti e basi pedagogiche — Adaptive Engine

Ultima revisione: **2026-09-11**.

TutorLab separa deliberatamente la propria policy ingegneristica dalle evidenze pedagogiche esterne. Le soglie in `config/adaptive-policy.json` sono default versionati e modificabili; non vengono presentate come standard scientifici universali.

## Education Endowment Foundation — Mastery learning

Fonte: https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/mastery-learning

Elementi recepiti nell'architettura:

- obiettivi di apprendimento chiari;
- diagnostic assessment per individuare punti di forza e debolezza;
- sequenziamento che costruisce sulle conoscenze fondazionali;
- monitoraggio regolare;
- supporto aggiuntivo quando uno studente non è ancora pronto ad avanzare;
- livello di padronanza alto prima del passaggio a nuovo contenuto.

Nota: EEF segnala variazione negli effetti e invita a considerare il contesto. TutorLab non interpreta quindi una percentuale singola come prova definitiva di mastery.

## Education Endowment Foundation — Feedback

Fonte: https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/feedback

Elementi recepiti:

- il feedback deve riferirsi a obiettivi e prestazione;
- deve offrire informazioni specifiche per migliorare;
- può riguardare task, processo e autoregolazione;
- va fornito anche quando il lavoro è corretto, non soltanto quando emerge un errore;
- formative assessment e feedback sono collegati perché le attività devono produrre informazioni utili su ciò che lo studente comprende.

TutorLab usa questa idea nel passaggio `evidence → inference → decision`: raccogliere un dato non serve se il sistema non sa come modificare il passo successivo.

## EEF — Embedding Formative Assessment

Fonte: https://educationendowmentfoundation.org.uk/projects-and-evaluation/promising-programmes/embedding-formative-assessment

Elementi recepiti:

- chiarire intenzioni di apprendimento e criteri di successo;
- usare domande e task per raccogliere evidenze;
- usare quelle evidenze per guidare il progresso;
- favorire ownership e feedback orientato all'azione.

## EEF — Adaptive teaching e feedback

Fonte: https://educationendowmentfoundation.org.uk/news/engine-room-of-adaptive-teaching

Il principio utile per TutorLab è che il valore del checking dipende da ciò che accade dopo: le evidenze devono poter portare a re-teaching, prosecuzione, estensione o ulteriore verifica.

## Decisioni specifiche di TutorLab

Le fonti precedenti non prescrivono:

- la nostra tassonomia esatta degli errori;
- le cinque decisioni `recover / consolidate / advance / extend / reassess`;
- il limite di profondità dello stack di recupero;
- le soglie numeriche della policy;
- il formato JSON degli eventi e degli stati.

Questi sono elementi progettuali originali di TutorLab, costruiti per rendere il sistema trasparente, verificabile e aggiornabile.

## Regola di revisione

Ogni modifica sostanziale alla policy adattiva deve indicare se deriva da:

1. nuova evidenza esterna;
2. risultati dei test interni;
3. osservazioni dei tutor;
4. modifica puramente tecnica.

In questo modo il repository conserva non soltanto **cosa** è cambiato, ma anche **perché**.