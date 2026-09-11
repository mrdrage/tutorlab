from __future__ import annotations

import math
import random
from fractions import Fraction

from engine.generation_common import open_task, phase_mode, task


def _rng(seed): return random.Random(seed)


def rational_decimal(phase,seed,band,support,task_id):
    r=_rng(seed); den=r.choice([2,4,5,8,10,20,25]); num=r.randint(1,den*2-1); f=Fraction(num,den); dec=float(f); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.rational-decimal.transfer",f"Confronta {f.numerator}/{f.denominator} e {dec:.3g}. Spiega se rappresentano lo stesso numero e quale rappresentazione useresti in un problema di misura.",band,support,params={"n":f.numerator,"d":f.denominator,"dec":dec},dimensions=["representation","explanation","strategy_selection"],acceptable="riconosce l'equivalenza e motiva la scelta della rappresentazione")
    return task(task_id,"math.y2.rational-decimal.convert",f"Scrivi come numero decimale {f.numerator}/{f.denominator}.",str(dec).replace('.',','),band,support,params={"n":f.numerator,"d":f.denominator},dimensions=["accuracy","representation"])


def ratios(phase,seed,band,support,task_id):
    r=_rng(seed); a=r.randint(2,8); k=r.randint(2,6); b=a*k; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.ratios.context",f"Una bevanda usa {a} parti di sciroppo ogni {b} parti d'acqua. Spiega cosa significa il rapporto {a}:{b} e scrivi un rapporto equivalente.",band,support,params={"a":a,"b":b,"k":k},dimensions=["conceptual_understanding","transfer","explanation"],acceptable=f"significato coerente e rapporto equivalente, per esempio {a*2}:{b*2}")
    return task(task_id,"math.y2.ratios.equivalent",f"Completa il rapporto equivalente: {a}:{b} = {a*2}:__.",str(b*2),band,support,params={"a":a,"b":b},dimensions=["accuracy","conceptual_understanding"])


def proportions(phase,seed,band,support,task_id):
    r=_rng(seed); a,b,c=r.randint(2,9),r.randint(2,9),r.randint(2,9); x=Fraction(b*c,a); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.proportions.strategy",f"Per risolvere {a}:{b} = {c}:x puoi usare prodotto incrociato, fattore di scala o riduzione all'unità. Scegli una strategia, trova x e spiega perché la proporzione è coerente.",band,support,params={"a":a,"b":b,"c":c},dimensions=["strategy_selection","accuracy","explanation"],acceptable=f"x={x.numerator}/{x.denominator} con strategia coerente")
    return task(task_id,"math.y2.proportions.solve",f"Trova x: {a}:{b} = {c}:x.",f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator),band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure"])


def percentages(phase,seed,band,support,task_id):
    r=_rng(seed); total=r.choice([80,100,120,200,250,400]); pct=r.choice([10,20,25,30,40,50]); part=total*pct//100; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.percentages.context",f"Un prezzo di {total} euro viene scontato del {pct}%. Calcola lo sconto e il nuovo prezzo, poi spiega perché il {pct}% deve essere riferito al prezzo iniziale.",band,support,params={"total":total,"pct":pct},dimensions=["accuracy","transfer","explanation"],acceptable=f"sconto {part}; nuovo prezzo {total-part}")
    return task(task_id,"math.y2.percentages.compute",f"Calcola il {pct}% di {total}.",str(part),band,support,params={"total":total,"pct":pct},dimensions=["accuracy","strategy_selection"])


def square_root(phase,seed,band,support,task_id):
    r=_rng(seed); n=r.randint(3,15); square=n*n; mode=phase_mode(phase)
    if mode=="transfer":
        non=square+r.randint(1,max(1,2*n-1)); low=math.isqrt(non)
        return open_task(task_id,"math.y2.sqrt.estimate",f"Senza calcolatrice, colloca √{non} tra due interi consecutivi e spiega il controllo con i quadrati.",band,support,params={"n":non,"low":low},dimensions=["reasoning","estimation","explanation"],acceptable=f"tra {low} e {low+1}")
    return task(task_id,"math.y2.sqrt.exact",f"Calcola √{square}.",str(n),band,support,params={"square":square},dimensions=["accuracy","conceptual_understanding"])


def irrational_awareness(phase,seed,band,support,task_id):
    r=_rng(seed); n=r.choice([2,3,5,6,7,8,10]); mode=phase_mode(phase)
    prompt=f"√{n} non è una radice esatta. Spiega la differenza tra il valore esatto √{n} e un'approssimazione decimale come {math.sqrt(n):.2f}."
    if mode=="transfer":
        return open_task(task_id,"math.y2.irrational.explain",prompt+" Indica anche tra quali due interi si trova.",band,support,params={"n":n},dimensions=["conceptual_understanding","explanation","reasoning"],acceptable="distingue valore esatto e approssimazione; collocazione coerente")
    return task(task_id,"math.y2.irrational.recognise",f"Vero o falso: {math.sqrt(n):.2f} è esattamente uguale a √{n}.","falso",band,support,params={"n":n},dimensions=["accuracy","conceptual_understanding"])


def powers_of_ten(phase,seed,band,support,task_id):
    r=_rng(seed); mant=r.randint(12,98)/10; exp=r.randint(2,5); value=mant*(10**exp); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.powers10.order",f"Confronta {mant}×10^{exp} e {mant}×10^{exp-2}. Di quanti ordini di grandezza differiscono? Spiega cosa cambia nel valore.",band,support,params={"mant":mant,"exp":exp},dimensions=["representation","reasoning","explanation"],acceptable="due ordini di grandezza; fattore 100")
    return task(task_id,"math.y2.powers10.value",f"Calcola {mant} × 10^{exp}.",str(value).replace('.',','),band,support,params={"mant":mant,"exp":exp},dimensions=["accuracy","representation"])


def sequences(phase,seed,band,support,task_id):
    r=_rng(seed); start=r.randint(1,8); step=r.randint(2,7); seq=[start+i*step for i in range(4)]; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.sequences.rule",f"La sequenza è {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... Descrivi la regola e trova il 10° termine senza elencare tutti i precedenti.",band,support,params={"start":start,"step":step},dimensions=["reasoning","generalisation","explanation"],acceptable=f"regola +{step}; decimo termine {start+9*step}")
    return task(task_id,"math.y2.sequences.next",f"Completa: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, __.",str(start+4*step),band,support,params={"start":start,"step":step},dimensions=["accuracy","pattern_recognition"])


def direct_proportionality(phase,seed,band,support,task_id):
    r=_rng(seed); k=r.randint(2,8); x=r.randint(2,9); y=k*x; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.direct-prop.represent",f"Una relazione segue y={k}x. Spiega come riconosceresti la proporzionalità diretta da una tabella e da un grafico, e interpreta il numero {k}.",band,support,params={"k":k},dimensions=["representation","conceptual_understanding","explanation"],acceptable="rapporto y/x costante; grafico passante per origine; k costante di proporzionalità")
    return task(task_id,"math.y2.direct-prop.compute",f"Se y={k}x, quanto vale y quando x={x}?",str(y),band,support,params={"k":k,"x":x},dimensions=["accuracy","representation"])


def inverse_proportionality(phase,seed,band,support,task_id):
    r=_rng(seed); k=r.choice([24,36,48,60,72]); x=r.choice([2,3,4,6]); y=k//x; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y2.inverse-prop.compare",f"Nella relazione xy={k}, spiega perché aumentando x diminuisce y ma non basta dire che 'è decrescente' per provare la proporzionalità inversa.",band,support,params={"k":k},dimensions=["conceptual_understanding","reasoning","explanation"],acceptable=f"il prodotto x·y deve restare costante e valere {k}")
    return task(task_id,"math.y2.inverse-prop.compute",f"Se x·y={k} e x={x}, trova y.",str(y),band,support,params={"k":k,"x":x},dimensions=["accuracy","conceptual_understanding"])


MATH_Y2_NUMBER_RELATION_BUILDERS={
    "math.numbers.rational-decimal-representations": rational_decimal,
    "math.numbers.ratios": ratios,
    "math.numbers.proportions": proportions,
    "math.numbers.percentages": percentages,
    "math.numbers.square-root": square_root,
    "math.numbers.irrational-awareness": irrational_awareness,
    "math.numbers.powers-of-ten": powers_of_ten,
    "math.relations.sequences": sequences,
    "math.relations.direct-proportionality": direct_proportionality,
    "math.relations.inverse-proportionality": inverse_proportionality,
}
