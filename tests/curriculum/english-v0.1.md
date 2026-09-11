# Acceptance test — Curriculum Inglese v0.1

Questi test valutano la qualità pedagogica del grafo, non soltanto la sua validità JSON.

## 1. Grammatica non equivale a competenza comunicativa

**Scenario:** studente di 1ª completa correttamente esercizi sul Present Simple ma, senza copione, non riesce a chiedere a un compagno cosa fa dopo scuola.

**Atteso:** TutorLab non marca automaticamente come solida l'interazione sulle routine. Mantiene distinta `eng.grammar.present_simple` da `eng.interaction.routine_exchanges` e propone pratica comunicativa guidata.

## 2. Diagnosi del listening: non sempre è vocabolario

**Scenario:** studente di 3ª conosce le parole di una breve conversazione quando le legge, ma non le riconosce nell'audio naturale.

**Atteso:** TutorLab considera `eng.phonology.connected_speech` e `eng.phonology.sentence_stress` come possibili colli di bottiglia prima di assegnare altro vocabolario.

## 3. Reading e distrattori

**Scenario:** studente trova spesso la parola identica tra domanda e testo e sceglie subito l'opzione corrispondente, sbagliando quando il significato è diverso.

**Atteso:** recupero su `eng.learning.gist_detail_notes` / strategia di verifica e, in terza, `eng.reading.a2_exam_strategies`. Non classificare automaticamente come lacuna grammaticale.

## 4. Narrazione passata

**Scenario:** studente sa raccontare l'ordine degli eventi ma evita tutti i verbi irregolari e passa al presente.

**Atteso:** bersaglio principale `eng.grammar.past_irregular`; mantenere l'obiettivo narrativo e ritornarvi dopo il recupero mirato.

## 5. Profilo asimmetrico

**Scenario:** studente di 3ª dimostra Reading A2 solido, Listening ancora fragile, Writing adeguato e buona interazione quotidiana.

**Atteso:** TutorLab conserva un profilo differenziato per modalità. Non riduce tutto a un singolo “livello inglese” né abbassa le abilità già solide.

## 6. INVALSI non sostituisce il curriculum

**Scenario:** studente ottiene ottimi risultati nei task Reading e Listening A2 ma non riesce a sostenere uno scambio orale semplice né a scrivere un'email comprensibile.

**Atteso:** le evidenze INVALSI rafforzano soltanto le dimensioni ricettive misurate. Speaking, interaction e writing restano da valutare separatamente.

## 7. Estensioni di terza non devono bloccare A2

**Scenario:** studente soddisfa evidenze A2 nelle attività comunicative ma non padroneggia il passivo o il reported speech semplice.

**Atteso:** `eng.grammar.passive_basic` e `eng.grammar.reported_speech_basic` sono `extension`; la loro assenza non impedisce da sola il riconoscimento di un profilo A2 coerente.

## 8. Mediazione non è copia

**Scenario:** studente deve dire a un compagno quale autobus prendere da un breve avviso e ripete quasi tutto il testo senza individuare linea e orario.

**Atteso:** TutorLab individua una difficoltà di selezione in mediazione e lavora su `eng.mediation.relay_specific_information`, non premia la quantità di testo riprodotto.

## 9. Riparazione della comunicazione

**Scenario:** in un role-play di viaggio lo studente dimentica una parola, si blocca e passa subito all'italiano nonostante conosca il resto della struttura.

**Atteso:** il bersaglio è `eng.learning.paraphrase_compensation`; il compito non viene automaticamente abbassato di livello.

## 10. Ritorno all'obiettivo dopo il recupero

**Scenario:** durante un'email A2 emergono errori sistematici nella costruzione delle domande che impediscono di rispondere a un invito.

**Atteso:** TutorLab recupera `eng.grammar.basic_questions` con attività brevi e poi ritorna all'email/interazione originaria. Il recupero non diventa una deviazione indefinita.

## 11. Competenza A2 come uso connesso

**Scenario:** studente conosce molti vocaboli e diverse regole ma produce soltanto frasi isolate.

**Atteso:** verificare `eng.grammar.connectors_cohesion`, `eng.production.experience_future_opinion` e/o i nodi writing pertinenti. La quantità di regole studiate non sostituisce la capacità di collegare significati.

## 12. Intercultura senza stereotipi

**Scenario:** da un breve testo su una scuola britannica lo studente conclude che “in Inghilterra tutti fanno sempre così”.

**Atteso:** TutorLab lavora su `eng.intercultural.compare_lifestyles` o `eng.intercultural.pragmatics_compare`, distinguendo esempio, tendenza e generalizzazione assoluta.

## Criterio di superamento del macro-blocco

Il curriculum inglese v0.1 è accettabile se consente di spiegare in modo coerente:

- quale prerequisito è fragile;
- se il problema riguarda sistema linguistico o uso comunicativo;
- quale competenza mantenere attiva;
- quale recupero mirato proporre;
- come ritornare all'obiettivo iniziale;
- quali evidenze supportano A1/A2 per ciascuna modalità.
