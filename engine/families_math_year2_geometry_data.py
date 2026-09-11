from __future__ import annotations

import random
from statistics import mean, median, multimode

from engine.generation_common import open_task, phase_mode, task


def _rng(seed): return random.Random(seed)


def area_concept(phase,seed,band,support,task_id):
    r=_rng(seed); a,b=r.randint(3,12),r.randint(2,10); area=a*b; per=2*(a+b); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.area-concept.explain",f"Un rettangolo misura {a} cm per {b} cm. Spiega perché area e perimetro descrivono grandezze diverse e indica unità corrette e valori.",band,support,params={"a":a,"b":b},dimensions=["conceptual_understanding","explanation","accuracy"],acceptable=f"area {area} cm²; perimetro {per} cm")
    return task(task_id,"math.y2.area-concept.compute",f"Qual è l'area di un rettangolo di lati {a} cm e {b} cm?",f"{area} cm²",band,support,params={"a":a,"b":b},dimensions=["accuracy","conceptual_understanding"])


def areas_polygons(phase,seed,band,support,task_id):
    r=_rng(seed); base=r.randint(4,14); height=r.randint(3,10); kind=r.choice(["triangolo","parallelogramma"]); area=base*height/2 if kind=="triangolo" else base*height; area_text=f"{area:g}"; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.areas.strategy",f"Una figura composta contiene un {kind} con base {base} cm e altezza {height} cm. Spiega quali misure servono davvero e come useresti scomposizione o ricomposizione per trovare l'area.",band,support,params={"kind":kind,"base":base,"height":height},dimensions=["strategy_selection","representation","explanation"],acceptable=f"formula coerente; area del {kind} {area_text} cm²")
    return task(task_id,"math.y2.areas.compute",f"Calcola l'area di un {kind} con base {base} cm e altezza {height} cm.",f"{area_text} cm²",band,support,params={"kind":kind,"base":base,"height":height},dimensions=["accuracy","procedure"])


def cartesian_plane(phase,seed,band,support,task_id):
    r=_rng(seed); x,y=r.randint(-6,6),r.randint(-6,6); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.cartesian.explain",f"Il punto P ha coordinate ({x}; {y}). Spiega quale numero indica lo spostamento orizzontale e quale quello verticale, e come cambierebbe il punto riflettendolo rispetto all'asse y.",band,support,params={"x":x,"y":y},dimensions=["representation","explanation","accuracy"],acceptable=f"ascissa {x}, ordinata {y}; riflesso ({-x}; {y})")
    return task(task_id,"math.y2.cartesian.read",f"Nel punto P({x}; {y}), qual è l'ordinata?",str(y),band,support,params={"x":x,"y":y},dimensions=["accuracy","representation"])


def pythagoras(phase,seed,band,support,task_id):
    r=_rng(seed); triple=r.choice([(3,4,5),(5,12,13),(6,8,10),(8,15,17)]); a,b,c=triple; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.pythagoras.transfer",f"Un triangolo rettangolo ha cateti {a} cm e {b} cm. Trova l'ipotenusa e spiega come riconosci quale lato deve stare da solo nella formula di Pitagora.",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","strategy_selection","explanation"],acceptable=f"ipotenusa {c} cm; è il lato opposto all'angolo retto")
    return task(task_id,"math.y2.pythagoras.compute",f"Triangolo rettangolo con cateti {a} cm e {b} cm: calcola l'ipotenusa.",f"{c} cm",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure"])


def transformations(phase,seed,band,support,task_id):
    r=_rng(seed); x,y=r.randint(1,6),r.randint(1,6); dx,dy=r.randint(1,4),r.randint(1,4); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.transformations.invariants",f"Il punto A({x};{y}) viene traslato di (+{dx};+{dy}). Trova A' e spiega quali proprietà geometriche di una figura restano invariate in una traslazione.",band,support,params={"x":x,"y":y,"dx":dx,"dy":dy},dimensions=["accuracy","reasoning","explanation"],acceptable=f"A'({x+dx};{y+dy}); lunghezze e angoli invariati")
    return task(task_id,"math.y2.transformations.translate",f"Trasla A({x};{y}) di (+{dx};+{dy}). Scrivi le coordinate di A'.",f"({x+dx}; {y+dy})",band,support,params={"x":x,"y":y,"dx":dx,"dy":dy},dimensions=["accuracy","representation"])


def similarity(phase,seed,band,support,task_id):
    r=_rng(seed); scale=r.choice([2,3,4]); side=r.randint(3,9); new=side*scale; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.similarity.scale",f"Due figure sono simili con fattore di scala {scale}. Un lato della prima misura {side} cm. Trova il corrispondente e spiega perché sommare {scale} non sarebbe corretto.",band,support,params={"scale":scale,"side":side},dimensions=["accuracy","conceptual_understanding","explanation"],acceptable=f"{new} cm; il fattore di scala moltiplica tutte le lunghezze corrispondenti")
    return task(task_id,"math.y2.similarity.compute",f"Fattore di scala {scale}: un lato di {side} cm diventa quanto?",f"{new} cm",band,support,params={"scale":scale,"side":side},dimensions=["accuracy","conceptual_understanding"])


def frequencies(phase,seed,band,support,task_id):
    r=_rng(seed); total=r.choice([20,25,40,50]); count=r.randint(2,total//2); rel=count/total; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.frequencies.compare",f"In un gruppo di {total} studenti, {count} scelgono l'opzione A. Calcola frequenza assoluta, relativa e percentuale e spiega quale useresti per confrontare gruppi di dimensioni diverse.",band,support,params={"total":total,"count":count},dimensions=["accuracy","representation","explanation"],acceptable=f"assoluta {count}; relativa {rel}; percentuale {rel*100:g}%; per confronti usare relativa/percentuale")
    return task(task_id,"math.y2.frequencies.relative",f"Su {total} osservazioni, {count} hanno una certa caratteristica. Qual è la frequenza relativa?",str(rel).replace('.',','),band,support,params={"total":total,"count":count},dimensions=["accuracy","representation"])


def central_tendency(phase,seed,band,support,task_id):
    r=_rng(seed); base=r.randint(3,9); data=[base,base+1,base+1,base+2,base+6]; m=mean(data); med=median(data); modes=multimode(data); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.central-tendency.choose",f"Dati: {data}. Calcola media, mediana e moda, poi spiega quale indice è più sensibile al valore alto {base+6}.",band,support,params={"data":data},dimensions=["accuracy","strategy_selection","explanation"],acceptable=f"media {m:g}; mediana {med:g}; moda {modes[0]}; la media è più sensibile agli estremi")
    return task(task_id,"math.y2.central-tendency.median",f"Trova la mediana dei dati {data}.",str(med).replace('.',','),band,support,params={"data":data},dimensions=["accuracy","procedure"])


def variability(phase,seed,band,support,task_id):
    r=_rng(seed); a=r.randint(2,6); spread=r.randint(4,10); data=[a,a+2,a+spread]; rng=max(data)-min(data); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.variability.compare",f"Per i dati {data}, calcola il campo di variazione e spiega perché conoscere solo la media non basta a descrivere quanto i dati sono dispersi.",band,support,params={"data":data},dimensions=["accuracy","reasoning","explanation"],acceptable=f"campo di variazione {rng}; la dispersione aggiunge informazione diversa dal centro")
    return task(task_id,"math.y2.variability.range",f"Calcola il campo di variazione dei dati {data}.",str(rng),band,support,params={"data":data},dimensions=["accuracy","conceptual_understanding"])


MATH_Y2_GEOMETRY_DATA_BUILDERS={
    "math.geometry.area-concept": area_concept,
    "math.geometry.areas-polygons": areas_polygons,
    "math.geometry.cartesian-plane": cartesian_plane,
    "math.geometry.pythagoras": pythagoras,
    "math.geometry.transformations-symmetry": transformations,
    "math.geometry.similarity": similarity,
    "math.data.frequencies": frequencies,
    "math.data.central-tendency": central_tendency,
    "math.data.variability": variability,
}
