from __future__ import annotations

import math
import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def circle(phase,seed,band,support,task_id):
    r=_r(seed); radius=r.randint(2,10); circ=2*radius; area=radius*radius
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.circle.explain",f"Un cerchio ha raggio {radius} cm. Esprimi lunghezza della circonferenza e area usando π, poi spiega perché le due formule hanno unità diverse.",band,support,params={"r":radius},dimensions=["accuracy","conceptual_understanding","explanation"],acceptable=f"circonferenza {circ}π cm; area {area}π cm²")
    return task(task_id,"math.y3.circle.area",f"Calcola in forma esatta l'area di un cerchio di raggio {radius} cm.",f"{area}π cm²",band,support,params={"r":radius},dimensions=["accuracy","procedure"])

def euclid(phase,seed,band,support,task_id):
    r=_r(seed); p=r.choice([4,9,16]); q=r.choice([9,16,25]); h=math.sqrt(p*q)
    ans=f"{h:g}"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.euclid.reason",f"Nel triangolo rettangolo l'altezza sull'ipotenusa divide l'ipotenusa in segmenti {p} cm e {q} cm. Usa il secondo teorema di Euclide per trovare l'altezza e collega la relazione alla similitudine.",band,support,params={"p":p,"q":q},dimensions=["accuracy","reasoning","representation","explanation"],acceptable=f"h²={p}·{q}; h={ans} cm")
    return task(task_id,"math.y3.euclid.compute",f"Le proiezioni sull'ipotenusa sono {p} cm e {q} cm. Calcola l'altezza relativa all'ipotenusa.",f"{ans} cm",band,support,params={"p":p,"q":q},dimensions=["accuracy","procedure"])

def solids(phase,seed,band,support,task_id):
    r=_r(seed); solid=r.choice([("prisma",5,10,7),("piramide",5,10,6),("cilindro",0,0,0)])
    name=solid[0]
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.solids.representation",f"Considera un {name}. Descrivi basi, altezza e tipo di superfici; spiega anche quale informazione cercheresti in uno sviluppo piano per riconoscere il solido.",band,support,params={"solid":name},dimensions=["spatial_reasoning","representation","explanation"],acceptable="descrizione coerente delle proprietà del solido")
    return task(task_id,"math.y3.solids.classify",f"Il {name} è un poliedro oppure un solido di rotazione?",("solido di rotazione" if name=="cilindro" else "poliedro"),band,support,params={"solid":name},dimensions=["accuracy","conceptual_understanding"])

def surface_area(phase,seed,band,support,task_id):
    r=_r(seed); a,b,h=r.randint(2,6),r.randint(2,6),r.randint(3,8); total=2*(a*b+a*h+b*h)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.surface-area.net",f"Un parallelepipedo rettangolo misura {a}×{b}×{h} cm. Calcola la superficie totale e spiega come lo sviluppo piano giustifica i sei rettangoli usati.",band,support,params={"a":a,"b":b,"h":h},dimensions=["accuracy","spatial_reasoning","explanation"],acceptable=f"{total} cm²")
    return task(task_id,"math.y3.surface-area.compute",f"Calcola la superficie totale di un parallelepipedo {a}×{b}×{h} cm.",f"{total} cm²",band,support,params={"a":a,"b":b,"h":h},dimensions=["accuracy","procedure"])

def volume(phase,seed,band,support,task_id):
    r=_r(seed); a,b,h=r.randint(2,7),r.randint(2,7),r.randint(3,9); v=a*b*h
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.volume.meaning",f"Una scatola rettangolare misura {a}×{b}×{h} cm. Calcola il volume e spiega perché l'unità è cubica e perché base×altezza descrive una struttura tridimensionale.",band,support,params={"a":a,"b":b,"h":h},dimensions=["accuracy","conceptual_understanding","explanation"],acceptable=f"{v} cm³")
    return task(task_id,"math.y3.volume.compute",f"Calcola il volume di un parallelepipedo {a}×{b}×{h} cm.",f"{v} cm³",band,support,params={"a":a,"b":b,"h":h},dimensions=["accuracy","procedure"])

def probability(phase,seed,band,support,task_id):
    r=_r(seed); total=r.choice([6,8,10,12]); fav=r.randint(1,total-1); g=math.gcd(fav,total); num,den=fav//g,total//g
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.probability.compare",f"In un esperimento ci sono {fav} esiti favorevoli su {total} equiprobabili. Esprimi la probabilità come frazione ridotta, decimale o percentuale e spiega perché una frequenza osservata in poche prove può essere diversa.",band,support,params={"fav":fav,"total":total},dimensions=["accuracy","reasoning","representation","explanation"],acceptable=f"{num}/{den}; probabilità teorica distinta dalla frequenza empirica")
    return task(task_id,"math.y3.probability.compute",f"Qual è la probabilità di un evento con {fav} casi favorevoli su {total} casi equiprobabili?",f"{num}/{den}",band,support,params={"fav":fav,"total":total},dimensions=["accuracy","conceptual_understanding"])

MATH_Y3_GEOMETRY_DATA_BUILDERS={
    "math.geometry.circle":circle,
    "math.geometry.euclid-theorems":euclid,
    "math.geometry.solids":solids,
    "math.geometry.surface-area":surface_area,
    "math.geometry.volume":volume,
    "math.data.elementary-probability":probability,
}
