# Session Engine v0.1

Il Session Engine trasforma un nodo curricolare e una decisione adattiva in una sessione didattica strutturata, quindi converte i risultati della sessione in evidence events per l'Adaptive Engine.

## Contratto

Input: nodo di competenza, azione adattiva, challenge band, durata, seed e fingerprint già utilizzati.

Output: session plan completo, student view senza soluzioni, task originali parametrizzati, rubriche per il tutor ed evidence events ricavati dai risultati.

## Sequenza per decisione

- `reassess`: raccoglie evidenza senza insegnare prima della misura.
- `recover`: lavora sul prerequisito e termina con una rivalutazione.
- `consolidate`: riduce la spiegazione e aumenta pratica mirata, fading e variazione.
- `advance`: attiva prerequisiti, introduce, modella, guida, rende autonomi e verifica il trasferimento.
- `extend`: aumenta scelta strategica, spiegazione e trasferimento senza anticipare automaticamente contenuti di anni successivi.

## Worked examples e fading

TutorLab evita il salto `spiegazione -> esercizi autonomi`. Quando opportuno usa `worked example -> faded example/guided practice -> independent practice`. Lo scaffolding è temporaneo e viene ridotto quando le evidenze mostrano maggiore autonomia.

## Diagnosi non contaminata

Una sessione `reassess` non presenta spiegazioni o soluzioni prima dei task diagnostici. Insegnare prima di misurare renderebbe ambigua l'evidenza sullo stato iniziale.

## Originalità e anti-ripetizione

Ogni task possiede un fingerprint calcolato da famiglia e parametri generativi. Il generatore confronta i fingerprint con la cronologia e tenta varianti diverse fino al limite configurato. L'obiettivo è evitare copie cosmetiche consecutive, non vietare la ripresa intenzionale di una struttura utile.

## Valutazione

Le risposte chiuse o strutturate possono essere valutate deterministicamente. Le risposte aperte richiedono uno score esterno, del tutor o di un futuro valutatore controllato: v0.1 non finge di poter attribuire automaticamente un giudizio affidabile a ogni produzione libera.

## Viste

Il session plan è un artefatto tutor e contiene soluzioni, rubriche e segnali diagnostici. `student_view()` rimuove queste informazioni prima della consegna allo studente.

## Vertical slice iniziali

- Matematica: `math.numbers.fraction-equivalence`.
- Inglese: `eng.grammar.present_simple`.

I due casi sono volutamente differenti: il primo verifica procedura, rappresentazione e ragionamento; il secondo distingue conoscenza della forma grammaticale e uso comunicativo.
