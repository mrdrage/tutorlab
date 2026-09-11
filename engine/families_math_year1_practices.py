from __future__ import annotations

import random

from engine.generation_common import open_task, phase_mode, task


def _rng(seed): return random.Random(seed)


def problem_representation(phase,seed,band,support,task_id):
    r=_rng(seed); apples=r.randint(18,40); boxes=r.randint(3,6); price=r.randint(2,5); mode=phase_mode(phase)
    prompt=f"Una scuola ha {apples} quaderni da distribuire in {boxes} scatole uguali. Ogni scatola costa {price} euro. Se la domanda è 'quanti quaderni vanno in ogni scatola?', quale dato è irrilevante?"
    if mode=="transfer":
        return open_task(task_id,"math.y1.problem-representation.model",f"Problema: {apples} quaderni, {boxes} scatole, {price} euro per scatola. Rappresenta solo i dati utili per sapere quanti quaderni mettere in ogni scatola e scrivi l'operazione senza eseguirla.",band,support,params={"items":apples,"boxes":boxes,"price":price},dimensions=["representation_demand","strategy_selection","explanation"],acceptable=f"{apples} ÷ {boxes}; il prezzo non serve")
    return task(task_id,"math.y1.problem-representation.select",prompt,f"{price} euro",band,support,params={"items":apples,"boxes":boxes,"price":price},dimensions=["accuracy","information_load","strategy_selection"])


def estimation(phase,seed,band,support,task_id):
    r=_rng(seed); a=r.randint(210,790); b=r.randint(110,590); exact=a+b; rounded=round(a,-2)+round(b,-2); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.estimation.plausibility",f"Un calcolo dà {a}+{b}= {exact+700}. Senza rifare il calcolo esatto, usa una stima per spiegare perché il risultato non è plausibile.",band,support,params={"a":a,"b":b},dimensions=["reasoning_demand","explanation","transfer"],acceptable=f"stima circa {rounded}, quindi {exact+700} è troppo grande")
    return task(task_id,"math.y1.estimation.round",f"Stima {a}+{b} arrotondando ciascun numero al centinaio più vicino.",str(rounded),band,support,params={"a":a,"b":b},dimensions=["accuracy","strategy_selection"])


def measurement_units(phase,seed,band,support,task_id):
    r=_rng(seed); cm=r.choice([120,250,340,475,620]); mode=phase_mode(phase); metres=cm/100
    if mode=="transfer":
        return open_task(task_id,"math.y1.measurement.choose-unit",f"Devi misurare la lunghezza di un'aula e lo spessore di una moneta. Scegli un'unità adatta per ciascuna misura e spiega perché non useresti la stessa unità in entrambi i casi.",band,support,params={"case":"room_coin"},dimensions=["strategy_selection","explanation","transfer"],acceptable="metri per l'aula; millimetri per la moneta, con motivazione sulla scala")
    answer=f"{metres:g} m"
    return task(task_id,"math.y1.measurement.convert",f"Converti {cm} cm in metri.",answer,band,support,params={"cm":cm},dimensions=["accuracy","procedure","precision_demand"])


PRACTICE_BUILDERS={
    "math.practice.problem-representation":problem_representation,
    "math.practice.estimation":estimation,
    "math.practice.measurement-units":measurement_units,
}
