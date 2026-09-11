from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def tool_selection(phase,seed,band,support,task_id):
    r=_r(seed); scenario=r.choice([
        ("stimare 198×51 prima del calcolo esatto","calcolo mentale/stima"),
        ("calcolare √173 con precisione al centesimo","calcolatrice dopo una stima"),
        ("confrontare l'andamento di una relazione per molti valori","tabella o software/grafico")])
    prompt,answer=scenario
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.tools.justify",f"Devi {prompt}. Scegli lo strumento più adatto, motiva la scelta e descrivi un controllo di plausibilità da fare sull'output.",band,support,params={"scenario":prompt},dimensions=["strategy_selection","precision","explanation"],acceptable=answer)
    return task(task_id,"math.y3.tools.choose",f"Per {prompt}, quale strumento useresti per primo?",answer,band,support,params={"scenario":prompt},dimensions=["strategy_selection","conceptual_understanding"])

def algorithmic_thinking(phase,seed,band,support,task_id):
    r=_r(seed); n=r.randint(3,9); result=2*n+3
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.algorithm.debug",f"Un algoritmo dice: prendi un numero n, raddoppialo e aggiungi 3. Per n={n} deve produrre {result}. Scrivi i passi in modo non ambiguo e proponi un caso limite o un test utile per controllarlo.",band,support,params={"n":n},dimensions=["process_depth","reasoning","precision","explanation"],acceptable="sequenza finita chiara con almeno un test di controllo")
    return task(task_id,"math.y3.algorithm.execute",f"Esegui l'algoritmo: prendi {n}, raddoppialo e aggiungi 3.",str(result),band,support,params={"n":n},dimensions=["accuracy","procedure"])

def integrated_problem_solving(phase,seed,band,support,task_id):
    r=_r(seed); price=r.choice([40,50,80]); discount=r.choice([10,20,25]); reduced=price*(100-discount)/100; people=r.choice([2,4,5]); each=reduced/people
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.integrated.solve",f"Un'attività costa {price} € e ha uno sconto del {discount}%. La spesa finale viene divisa tra {people} persone. Determina la quota per persona, scegli tu la strategia, indica un controllo di plausibilità e spiega quali informazioni sono matematicamente essenziali.",band,support,params={"price":price,"discount":discount,"people":people},dimensions=["strategy_selection","transfer","accuracy","explanation"],acceptable=f"totale {reduced:g} €; quota {each:g} €")
    return task(task_id,"math.y3.integrated.check",f"Dopo uno sconto del {discount}% su {price} €, qual è il prezzo finale?",f"{reduced:g} €",band,support,params={"price":price,"discount":discount},dimensions=["accuracy","strategy_selection"])

MATH_Y3_PRACTICE_BUILDERS={
    "math.practice.tool-selection":tool_selection,
    "math.practice.algorithmic-thinking":algorithmic_thinking,
    "math.practice.integrated-problem-solving":integrated_problem_solving,
}
