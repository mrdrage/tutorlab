from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def modelling(phase,seed,band,support,task_id):
    r=random.Random(seed); unit=r.randint(2,8); fixed=r.randint(1,5); n=r.randint(3,10)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y2.modelling.open",f"Un'attività costa {unit} euro per partecipante più {fixed} euro fissi. Scrivi un modello del costo totale in funzione di n, spiega i termini e indica un'ipotesi del modello.",band,support,params={"unit":unit,"fixed":fixed},dimensions=["modelling","explanation","transfer"],acceptable=f"C={unit}n+{fixed}, con interpretazione coerente")
    return task(task_id,"math.y2.modelling.compute",f"Il costo è {unit} euro per persona più {fixed} euro fissi. Calcola il totale per {n} persone.",str(unit*n+fixed),band,support,params={"unit":unit,"fixed":fixed,"n":n},dimensions=["accuracy","modelling"])


def argumentation(phase,seed,band,support,task_id):
    r=random.Random(seed); example=r.choice(["la somma di due numeri pari è pari","un multiplo di 6 è anche multiplo di 3","un numero che termina per 0 è divisibile per 5"])
    return open_task(task_id,"math.y2.argumentation.general",f"Spiega in modo generale perché è valida questa proprietà: {example}. Una semplice verifica numerica non basta.",band,support,params={"property":example},dimensions=["reasoning","argumentation","explanation"],acceptable="giustificazione generale coerente con la proprietà")


MATH_Y2_PRACTICE_BUILDERS={
    "math.practice.modelling":modelling,
    "math.practice.argumentation":argumentation,
}
