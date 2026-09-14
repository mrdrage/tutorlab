from __future__ import annotations

import random

from engine.families_upper_secondary import _index, _rubric
from engine.generation_common import open_task, phase_mode, task


def _case_builder(cid, family, cases):
    def build(phase, seed, band, support, task_id):
        node=_index("mathematics")[cid]; mode=phase_mode(phase); rng=random.Random(seed)
        prompt,answer=rng.choice(cases); rubric=_rubric(node,node["title"])
        params={"competency":cid,"phase":phase,"seed":seed,"case_family":family}
        errors=node.get("diagnostic_signals",[])
        if mode=="model":
            return open_task(task_id,f"upper.math.{family}.model",f"Esempio svolto: {prompt} Risposta del modello: {answer}. Ricostruisci e giustifica il passaggio decisivo.",band,support,params=params,dimensions=["accuracy","explanation","reasoning"],rubric=rubric,acceptable="ricostruzione coerente del modello",errors=errors)
        if mode=="transfer":
            return open_task(task_id,f"upper.math.{family}.transfer",f"{prompt} Risolvi e poi spiega perché questa strategia è appropriata; indica anche un controllo del risultato.",band,support,params=params,dimensions=["accuracy","transfer","reasoning"],rubric=rubric,acceptable=answer,errors=errors)
        return task(task_id,f"upper.math.{family}.{mode}",prompt,answer,band,support,params=params,dimensions=["accuracy","independence","reasoning"],rubric=rubric,errors=errors)
    return build


CASES={
"math.us.algebra.symbolic-control":("symbolic-control",[("Semplifica 3(x-2)+2x-(x+1).","4x-7"),("Semplifica 2(3x+1)-4(x-2).","2x+10")]),
"math.us.algebra.systems-linear":("systems",[("Risolvi il sistema x+y=7, x-y=1.","x=4, y=3"),("Risolvi il sistema 2x+y=8, x-y=1.","x=3, y=2")]),
"math.us.algebra.radicals":("radicals",[("Semplifica √72.","6√2"),("Semplifica √50.","5√2")]),
"math.us.algebra.factorisation":("factorisation",[("Scomponi x^2-9.","(x-3)(x+3)"),("Scomponi x^2+5x+6.","(x+2)(x+3)")]),
"math.us.functions.function-concept":("function-concept",[("La relazione associa a ogni x il valore y=2x+1. Spiega perché è una funzione e calcola y per x=3.","è funzione; y=7"),("Una tabella assegna a x=1,2,3 rispettivamente y=4,4,5. Può rappresentare una funzione di x?","sì")]),
"math.us.functions.quadratic-functions":("quadratic-function",[("Per y=x^2-4x+3 indica gli zeri.","x=1 e x=3"),("Per y=x^2-6x+8 indica gli zeri.","x=2 e x=4")]),
"math.us.data.probability-foundations":("probability",[("Un dado equo viene lanciato una volta. Qual è la probabilità di ottenere un numero pari?","1/2"),("Da un sacchetto con 3 palline rosse e 2 blu se ne estrae una. Probabilità di blu?","2/5")]),
"math.us.algebra.rational-expressions":("rational-domain",[("Per (x+1)/(x-2), indica la condizione di esistenza.","x≠2"),("Per (2x)/(x+3), indica la condizione di esistenza.","x≠-3")]),
"math.us.functions.polynomial-rational":("rational-function",[("Per f(x)=(x-1)/(x+2), indica zero e valore escluso dal dominio.","zero x=1; escluso x=-2"),("Per f(x)=(x+3)/(x-4), indica zero e valore escluso dal dominio.","zero x=-3; escluso x=4")]),
"math.us.data.conditional-probability-intro":("conditional-probability",[("In una classe 12 studenti fanno sport; 8 di questi giocano a calcio. Sapendo che uno studente scelto fa sport, qual è la probabilità che giochi a calcio?","2/3"),("Tra 15 persone con patente, 5 guidano ogni giorno. Sapendo che la persona scelta ha la patente, probabilità che guidi ogni giorno?","1/3")]),
"math.us.trigonometry.functions":("trig-functions",[("Quanto vale sin(30°)?","1/2"),("Quanto vale cos(60°)?","1/2")]),
"math.us.functions.precalculus-analysis":("precalculus",[("Per f(x)=(x-1)/(x+2), indica dominio, zero e asintoto verticale.","dominio x≠-2; zero x=1; asintoto x=-2"),("Per f(x)=(x+1)/(x-3), indica dominio, zero e asintoto verticale.","dominio x≠3; zero x=-1; asintoto x=3")]),
"math.us.data.combinatorics-probability":("combinatorics",[("Quante sequenze di due lettere diverse puoi formare scegliendo da A,B,C?","6"),("Quante coppie non ordinate puoi scegliere da 4 persone?","6")]),
"math.us.data.statistical-reasoning":("statistical-reasoning",[("Due gruppi hanno la stessa media 10; il gruppo A ha valori molto più dispersi. Quale informazione distingue meglio i gruppi?","una misura di variabilità"),("Un grafico mostra associazione tra ore di studio e voto. Puoi concludere da solo che più studio causa sempre voti più alti?","no")]),
"math.us.functions.model-comparison":("model-comparison",[("Una quantità cresce di 5 ogni mese. È più naturale un modello lineare o esponenziale?","lineare"),("Una popolazione aumenta del 8% ogni anno. È più naturale un modello lineare o esponenziale?","esponenziale")]),
"math.us.scientifico.geometry.vectors":("vectors",[("Dato v=(3,4), calcola il modulo.","5"),("Dati u=(2,1) e v=(1,3), calcola u+v.","(3,4)")]),
"math.us.scientifico.functions.transformations":("function-transformations",[("Se g(x)=f(x)+3, quale trasformazione subisce il grafico di f?","traslazione verso l'alto di 3"),("Se g(x)=f(x-2), quale trasformazione subisce il grafico di f?","traslazione verso destra di 2")]),
"math.us.scientifico.probability.random-variables":("random-variables",[("X vale 0 con probabilità 0,4 e 2 con probabilità 0,6. Calcola E[X].","1.2"),("X vale 1 con probabilità 0,5 e 3 con probabilità 0,5. Calcola E[X].","2")])
}

UPPER_MATH_OVERRIDES={cid:_case_builder(cid,family,cases) for cid,(family,cases) in CASES.items()}
