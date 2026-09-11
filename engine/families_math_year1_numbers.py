from __future__ import annotations

import math
import random
from fractions import Fraction

from engine.generation_common import open_task, phase_mode, task


def _rng(seed): return random.Random(seed)


def natural_number_sense(phase,seed,band,support,task_id):
    r=_rng(seed); mode=phase_mode(phase); a=r.randint(120,9800); b=a+r.randint(10,900)
    if mode=="transfer":
        return open_task(task_id,"math.y1.number-sense.transfer",f"Due contatori mostrano {a} e {b}. Spiega quale valore è maggiore e indica un modo per verificarlo senza fare una sottrazione completa.",band,support,params={"a":a,"b":b},dimensions=["accuracy","explanation","strategy_selection"],acceptable=f"{b} è maggiore; confronto per valore posizionale o retta dei numeri")
    if mode=="model":
        return task(task_id,"math.y1.number-sense.model",f"Osserva {a} e {b}: confronta prima le migliaia, poi centinaia, decine e unità. Qual è il maggiore?",str(max(a,b)),band,"worked_support",params={"a":a,"b":b},dimensions=["accuracy","conceptual_understanding"])
    return task(task_id,"math.y1.number-sense.compare",f"Scrivi il numero maggiore tra {a} e {b}.",str(max(a,b)),band,support,params={"a":a,"b":b},dimensions=["accuracy","independence"])


def natural_operations(phase,seed,band,support,task_id):
    r=_rng(seed); op=r.choice(["+","-","×","÷"]); mode=phase_mode(phase)
    if op=="+": a,b=r.randint(120,900),r.randint(20,400); ans=a+b
    elif op=="-": a,b=r.randint(300,900),r.randint(20,250); ans=a-b
    elif op=="×": a,b=r.randint(12,60),r.randint(3,15); ans=a*b
    else: b=r.randint(3,15); ans=r.randint(4,40); a=b*ans
    if mode=="transfer":
        return open_task(task_id,"math.y1.operations.transfer",f"In un problema compare il calcolo {a} {op} {b}. Inventa una situazione reale coerente e spiega cosa rappresenta il risultato {ans}.",band,support,params={"a":a,"b":b,"op":op},dimensions=["transfer","explanation","strategy_selection"],acceptable=f"problema coerente con {a} {op} {b} = {ans}")
    return task(task_id,"math.y1.operations.compute",f"Calcola {a} {op} {b}.",str(ans),band,support,params={"a":a,"b":b,"op":op},dimensions=["accuracy","procedure","independence"])


def numeric_expressions(phase,seed,band,support,task_id):
    r=_rng(seed); a,b,c=r.randint(2,12),r.randint(2,9),r.randint(2,9); expr=f"{a} + {b} × {c}"; ans=a+b*c; mode=phase_mode(phase)
    if mode=="transfer":
        wrong=(a+b)*c
        return open_task(task_id,"math.y1.expressions.error-analysis",f"Uno studente calcola {expr} e ottiene {wrong}. Spiega l'errore e trova il risultato corretto.",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","explanation","conceptual_understanding"],acceptable=f"prima {b}×{c}, poi +{a}; risultato {ans}",errors=[{"pattern":"left_to_right","code":"procedure_error"}])
    if mode=="model":
        return task(task_id,"math.y1.expressions.model",f"Valuta {expr}. Primo passaggio: calcola {b} × {c}; poi aggiungi {a}.",str(ans),band,"worked_support",params={"a":a,"b":b,"c":c},dimensions=["procedure","accuracy"])
    return task(task_id,"math.y1.expressions.evaluate",f"Calcola rispettando le precedenze: {expr}.",str(ans),band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure","independence"])


def powers(phase,seed,band,support,task_id):
    r=_rng(seed); base=r.randint(2,8); exp=r.randint(2,4); ans=base**exp; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.powers.explain",f"Spiega perché {base}^{exp} non significa {base}×{exp}. Scrivi anche il prodotto ripetuto corretto.",band,support,params={"base":base,"exp":exp},dimensions=["conceptual_understanding","explanation"],acceptable="potenza come prodotto della base ripetuta per il numero di fattori indicato dall'esponente")
    return task(task_id,"math.y1.powers.evaluate",f"Calcola {base}^{exp}.",str(ans),band,support,params={"base":base,"exp":exp},dimensions=["accuracy","conceptual_understanding"])


def divisibility(phase,seed,band,support,task_id):
    r=_rng(seed); divisor=r.choice([2,3,5,9,10]); k=r.randint(12,80); n=divisor*k; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.divisibility.reason",f"Senza eseguire la divisione completa, giustifica perché {n} è divisibile per {divisor}.",band,support,params={"n":n,"divisor":divisor},dimensions=["reasoning_demand","explanation","accuracy"],acceptable=f"applicazione corretta di un criterio o riconoscimento che {n}={divisor}×{k}")
    return task(task_id,"math.y1.divisibility.check",f"{n} è divisibile per {divisor}? Rispondi sì o no.","sì",band,support,params={"n":n,"divisor":divisor},dimensions=["accuracy","strategy_selection"])


def prime_factorization(phase,seed,band,support,task_id):
    r=_rng(seed); p,q=r.choice([(2,3),(2,5),(3,5),(2,7)]); a,b=r.randint(1,3),r.randint(1,2); n=(p**a)*(q**b); ans=f"{p}^{a} × {q}^{b}" if a>1 or b>1 else f"{p} × {q}"; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.prime-factorization.check",f"Una scomposizione di {n} termina con un fattore composto. Spiega perché non è ancora una scomposizione in fattori primi e indica come controllare il risultato finale.",band,support,params={"n":n,"p":p,"q":q,"a":a,"b":b},dimensions=["conceptual_understanding","explanation","procedure"],acceptable="tutti i fattori finali devono essere primi; controllo moltiplicando i fattori")
    return task(task_id,"math.y1.prime-factorization.factor",f"Scomponi {n} in fattori primi. Usa potenze quando un fattore si ripete.",ans,band,support,params={"n":n,"p":p,"q":q,"a":a,"b":b},dimensions=["accuracy","procedure"])


def gcd_lcm(phase,seed,band,support,task_id):
    r=_rng(seed); a,b=r.choice([(12,18),(18,24),(20,30),(24,36),(15,25)]); g=math.gcd(a,b); l=abs(a*b)//g; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.gcd-lcm.context",f"Due eventi si ripetono ogni {a} e {b} minuti. Se partono insieme, dopo quanti minuti coincidono di nuovo? Spiega perché serve mcm e non MCD.",band,support,params={"a":a,"b":b},dimensions=["strategy_selection","transfer","explanation"],acceptable=f"mcm({a},{b})={l}")
    which=r.choice(["MCD","mcm"]); ans=g if which=="MCD" else l
    return task(task_id,"math.y1.gcd-lcm.compute",f"Calcola {which}({a}, {b}).",str(ans),band,support,params={"a":a,"b":b,"which":which},dimensions=["accuracy","procedure"])


def fraction_meaning(phase,seed,band,support,task_id):
    r=_rng(seed); d=r.randint(3,8); n=r.randint(1,d-1); mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.fraction-meaning.context",f"Inventa due situazioni diverse in cui la frazione {n}/{d} abbia senso: una come parte di un intero e una come quoziente.",band,support,params={"n":n,"d":d},dimensions=["conceptual_understanding","transfer","explanation"],acceptable="due interpretazioni coerenti della stessa frazione")
    return task(task_id,"math.y1.fraction-meaning.read",f"Una torta è divisa in {d} parti uguali e ne vengono prese {n}. Quale frazione della torta è stata presa?",f"{n}/{d}",band,support,params={"n":n,"d":d},dimensions=["accuracy","conceptual_understanding"])


def fraction_comparison(phase,seed,band,support,task_id):
    r=_rng(seed); a,b,c,d=r.randint(1,5),r.randint(3,9),r.randint(1,5),r.randint(3,9)
    f1,f2=Fraction(a,b),Fraction(c,d)
    if f1==f2: c=max(1,c-1); f2=Fraction(c,d)
    answer=f"{a}/{b}" if f1>f2 else f"{c}/{d}"; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.fraction-comparison.explain",f"Confronta {a}/{b} e {c}/{d} scegliendo tu una strategia e giustifica la scelta.",band,support,params={"a":a,"b":b,"c":c,"d":d},dimensions=["accuracy","strategy_selection","explanation"],acceptable=f"la frazione maggiore è {answer}")
    return task(task_id,"math.y1.fraction-comparison.choose",f"Quale frazione è maggiore: {a}/{b} oppure {c}/{d}?",answer,band,support,params={"a":a,"b":b,"c":c,"d":d},dimensions=["accuracy","strategy_selection"])


def fraction_operations(phase,seed,band,support,task_id):
    r=_rng(seed); op=r.choice(["+","-","×","÷"]); x=Fraction(r.randint(1,5),r.randint(2,8)); y=Fraction(r.randint(1,5),r.randint(2,8))
    if op=="+": z=x+y
    elif op=="-":
        if x<y: x,y=y,x
        z=x-y
    elif op=="×": z=x*y
    else:
        if y==0: y=Fraction(1,2)
        z=x/y
    a=f"{x.numerator}/{x.denominator}"; b=f"{y.numerator}/{y.denominator}"; ans=f"{z.numerator}/{z.denominator}"; mode=phase_mode(phase)
    if mode=="transfer":
        return open_task(task_id,"math.y1.fraction-operations.error-analysis",f"Spiega quale regola useresti per calcolare {a} {op} {b} e perché quella regola è adatta proprio a questa operazione.",band,support,params={"a":a,"b":b,"op":op},dimensions=["procedure","explanation","strategy_selection"],acceptable=f"procedura corretta; risultato {ans}")
    return task(task_id,"math.y1.fraction-operations.compute",f"Calcola e riduci ai minimi termini: {a} {op} {b}.",ans,band,support,params={"a":a,"b":b,"op":op},dimensions=["accuracy","procedure","independence"])


NUMBER_BUILDERS={
    "math.numbers.natural-number-sense":natural_number_sense,
    "math.numbers.natural-operations":natural_operations,
    "math.numbers.numeric-expressions-natural":numeric_expressions,
    "math.numbers.powers-natural":powers,
    "math.numbers.divisibility":divisibility,
    "math.numbers.prime-factorization":prime_factorization,
    "math.numbers.gcd-lcm":gcd_lcm,
    "math.numbers.fraction-meaning":fraction_meaning,
    "math.numbers.fraction-comparison":fraction_comparison,
    "math.numbers.fraction-operations":fraction_operations,
}
