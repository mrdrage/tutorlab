from __future__ import annotations

import random

from engine.generation_common import open_task, phase_mode, task


def _rng(seed): return random.Random(seed)


def basic_objects(phase,seed,band,support,task_id):
    r=_rng(seed); mode=phase_mode(phase); relation=r.choice([("rette parallele","non si incontrano"),("rette perpendicolari","formano quattro angoli retti"),("segmento","ha due estremi")])
    if mode=="transfer":
        return open_task(task_id,"math.y1.geometry.basic.transfer",f"Descrivi con parole precise una figura che contenga {relation[0]} e spiega quale proprietà deve essere visibile.",band,support,params={"concept":relation[0]},dimensions=["representation_demand","explanation"],acceptable=relation[1])
    return task(task_id,"math.y1.geometry.basic.recognize",f"Quale descrizione è corretta per {relation[0]}?",relation[1],band,support,params={"concept":relation[0]},dimensions=["accuracy","conceptual_understanding"])


def angles(phase,seed,band,support,task_id):
    r=_rng(seed); a=r.choice([25,35,45,55,70]); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.geometry.angles.reason",f"Due angoli sono complementari e uno misura {a}°. Trova l'altro e spiega la relazione usata.",band,support,params={"a":a},dimensions=["accuracy","reasoning_demand","explanation"],acceptable=f"{90-a}° perché la somma è 90°")
    kind="acuto" if a<90 else "retto" if a==90 else "ottuso"
    return task(task_id,"math.y1.geometry.angles.classify",f"Classifica un angolo di {a}°.",kind,band,support,params={"a":a},dimensions=["accuracy","conceptual_understanding"])


def polygons(phase,seed,band,support,task_id):
    r=_rng(seed); sides=r.choice([3,4,5,6,8]); names={3:"triangolo",4:"quadrilatero",5:"pentagono",6:"esagono",8:"ottagono"}; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.geometry.polygons.explain",f"Spiega perché una figura con {sides} lati appartiene alla famiglia dei {names[sides]} e indica una proprietà che non dipende da come è ruotata nel foglio.",band,support,params={"sides":sides},dimensions=["conceptual_understanding","representation_demand","explanation"],acceptable=f"ha {sides} lati; classificazione basata sulle proprietà")
    return task(task_id,"math.y1.geometry.polygons.name",f"Come si chiama un poligono con {sides} lati?",names[sides],band,support,params={"sides":sides},dimensions=["accuracy","conceptual_understanding"])


def triangles_quadrilaterals(phase,seed,band,support,task_id):
    r=_rng(seed); mode=phase_mode(phase); item=r.choice([("quadrato","quattro lati uguali e quattro angoli retti"),("rettangolo","quattro angoli retti e lati opposti uguali"),("rombo","quattro lati uguali"),("triangolo isoscele","almeno due lati uguali")])
    if mode=="transfer":
        return open_task(task_id,"math.y1.geometry.classification.reason",f"Spiega perché un quadrato può essere considerato anche un rettangolo. Quale proprietà del rettangolo soddisfa?",band,support,params={"case":"square_rectangle"},dimensions=["reasoning_demand","conceptual_understanding","explanation"],acceptable="ha quattro angoli retti; la classificazione per proprietà permette inclusioni")
    return task(task_id,"math.y1.geometry.classification.identify",f"Quale figura è descritta così: {item[1]}?",item[0],band,support,params={"description":item[1]},dimensions=["accuracy","conceptual_understanding"])


def perimeter(phase,seed,band,support,task_id):
    r=_rng(seed); a,b=r.randint(3,14),r.randint(3,14); p=2*(a+b); mode=phase_mode(phase)
    if mode=="transfer":
        missing=r.randint(3,12); total=2*(a+missing)
        return open_task(task_id,"math.y1.geometry.perimeter.inverse",f"Un rettangolo ha perimetro {total} cm e un lato lungo {a} cm. Trova l'altro lato e spiega il procedimento.",band,support,params={"a":a,"total":total},dimensions=["accuracy","strategy_selection","transfer","explanation"],acceptable=f"{missing} cm")
    return task(task_id,"math.y1.geometry.perimeter.compute",f"Un rettangolo misura {a} cm per {b} cm. Calcola il perimetro.",f"{p} cm",band,support,params={"a":a,"b":b},dimensions=["accuracy","procedure"])


def tables_charts(phase,seed,band,support,task_id):
    r=_rng(seed); values=[r.randint(2,12) for _ in range(4)]; labels=["A","B","C","D"]; m=max(values); idx=values.index(m); mode=phase_mode(phase)
    table=", ".join(f"{l}:{v}" for l,v in zip(labels,values))
    if mode=="transfer":
        return open_task(task_id,"math.y1.data.interpret",f"Dati: {table}. Formula una conclusione corretta e una conclusione che NON è possibile ricavare da questi dati, spiegando la differenza.",band,support,params={"values":values},dimensions=["representation_demand","reasoning_demand","explanation"],acceptable=f"{labels[idx]} ha il valore massimo {m}; evitare inferenze non presenti")
    return task(task_id,"math.y1.data.read",f"Leggi la tabella {table}. Quale categoria ha il valore maggiore?",labels[idx],band,support,params={"values":values},dimensions=["accuracy","representation_demand"])


GEOMETRY_DATA_BUILDERS={
    "math.geometry.basic-objects":basic_objects,
    "math.geometry.angles":angles,
    "math.geometry.polygons":polygons,
    "math.geometry.triangles-quadrilaterals":triangles_quadrilaterals,
    "math.geometry.perimeter":perimeter,
    "math.data.tables-charts":tables_charts,
}
