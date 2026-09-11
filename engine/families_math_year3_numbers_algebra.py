from __future__ import annotations

import random
from fractions import Fraction

from engine.generation_common import open_task, phase_mode, task


def _r(seed):
    return random.Random(seed)


def signed_number_sense(phase, seed, band, support, task_id):
    r=_r(seed); a=-r.randint(2,15); b=-r.randint(2,15)
    if a==b: b-=1
    greater=max(a,b)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.signed-sense.explain",f"Confronta {a} e {b} usando la retta dei numeri e spiega perché tra due negativi il numero con valore assoluto maggiore non è il maggiore.",band,support,params={"a":a,"b":b},dimensions=["accuracy","conceptual_understanding","explanation"],acceptable=f"{greater} è maggiore; sulla retta è più a destra")
    return task(task_id,"math.y3.signed-sense.compare",f"Qual è il maggiore tra {a} e {b}?",str(greater),band,support,params={"a":a,"b":b},dimensions=["accuracy","conceptual_understanding"])


def signed_operations(phase, seed, band, support, task_id):
    r=_r(seed); a=r.randint(-12,12) or 4; b=r.randint(-10,10) or -3; op=r.choice(["+","-","×"])
    ans={"+":a+b,"-":a-b,"×":a*b}[op]
    if phase_mode(phase)=="transfer":
        wrong=abs(a)+abs(b) if op in {"+","-"} else abs(a*b)
        return open_task(task_id,"math.y3.signed-ops.error",f"Uno studente calcola {a} {op} ({b}) e ottiene {wrong}. Controlla il risultato, individua l'eventuale errore sui segni e spiega una strategia di verifica.",band,support,params={"a":a,"b":b,"op":op},dimensions=["accuracy","procedure","explanation"],acceptable=f"risultato corretto {ans}; controllo coerente con significato dei segni")
    return task(task_id,"math.y3.signed-ops.compute",f"Calcola: {a} {op} ({b}).",str(ans),band,support,params={"a":a,"b":b,"op":op},dimensions=["accuracy","procedure"])


def rational_expressions(phase, seed, band, support, task_id):
    r=_r(seed); a=r.randint(-6,6) or 2; b=r.randint(2,7); c=r.randint(-5,5) or -2
    value=Fraction(a,b)+c
    ans=f"{value.numerator}/{value.denominator}" if value.denominator!=1 else str(value.numerator)
    expr=f"{a}/{b} + ({c})"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.rational-expr.strategy",f"Per calcolare {expr}, descrivi l'ordine dei passaggi, indica dove è più facile perdere un segno e trova il risultato ridotto ai minimi termini.",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure","strategy_selection","explanation"],acceptable=f"procedura coerente e risultato {ans}")
    return task(task_id,"math.y3.rational-expr.compute",f"Calcola e semplifica: {expr}.",ans,band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure","precision"])


def real_number_system(phase, seed, band, support, task_id):
    r=_r(seed); sample=r.choice([("-4","intero"),("3/5","razionale"),("√2","irrazionale"),("7","naturale")])
    value,smallest=sample
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.number-system.classify",f"Classifica {value} nel più piccolo insieme numerico appropriato e spiega in quali insiemi più ampi è comunque contenuto.",band,support,params={"value":value,"smallest":smallest},dimensions=["conceptual_understanding","reasoning","explanation"],acceptable=f"insieme minimo: {smallest}; inclusioni coerenti")
    return task(task_id,"math.y3.number-system.choose",f"Qual è il più piccolo insieme tra naturale, intero, razionale e irrazionale che contiene {value}?",smallest,band,support,params={"value":value},dimensions=["accuracy","conceptual_understanding"])


def symbolic_generalization(phase, seed, band, support, task_id):
    r=_r(seed); step=r.randint(2,5); start=r.randint(1,4)
    terms=[start+step*i for i in range(4)]
    formula=f"{start} + {step}(n-1)"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.symbolic-generalization.formula",f"La sequenza è {terms}. Costruisci una formula per il termine in posizione n, verifica la formula per n=4 e spiega che cosa rappresenta la lettera n.",band,support,params={"start":start,"step":step},dimensions=["symbolic_reasoning","accuracy","explanation"],acceptable=f"formula equivalente a {formula}; n rappresenta la posizione")
    return task(task_id,"math.y3.symbolic-generalization.next",f"La sequenza {terms} cresce sempre dello stesso passo. Qual è il termine successivo?",str(start+step*4),band,support,params={"start":start,"step":step},dimensions=["accuracy","pattern_reasoning"])


def algebraic_expressions(phase, seed, band, support, task_id):
    r=_r(seed); a=r.randint(2,6); b=r.randint(-5,5) or 3; x=r.randint(-4,4) or -2; ans=a*x+b
    expr=f"{a}x {'+' if b>=0 else '-'} {abs(b)}"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.algebra.substitution",f"Valuta {expr} per x={x}. Mostra perché, se x è negativo, è utile sostituire il valore tra parentesi e controlla il risultato.",band,support,params={"a":a,"b":b,"x":x},dimensions=["accuracy","procedure","explanation"],acceptable=f"{ans}")
    return task(task_id,"math.y3.algebra.evaluate",f"Calcola il valore di {expr} per x={x}.",str(ans),band,support,params={"a":a,"b":b,"x":x},dimensions=["accuracy","procedure"])


def first_degree_equations(phase, seed, band, support, task_id):
    r=_r(seed); solution=r.randint(-6,8) or 3; a=r.randint(2,6); b=r.randint(-8,8); c=a*solution+b
    equation=f"{a}x {'+' if b>=0 else '-'} {abs(b)} = {c}"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.equations.verify",f"Risolvi {equation}. Poi verifica la soluzione sostituendola nei due membri e spiega perché fare la stessa operazione su entrambi i membri conserva l'uguaglianza.",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure","conceptual_understanding","explanation"],acceptable=f"x={solution}; verifica corretta")
    return task(task_id,"math.y3.equations.solve",f"Risolvi: {equation}.",f"x={solution}",band,support,params={"a":a,"b":b,"c":c},dimensions=["accuracy","procedure"])


def multiple_representations(phase, seed, band, support, task_id):
    r=_r(seed); k=r.randint(2,5); x=r.randint(2,6); y=k*x
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.multirep.translate",f"La relazione è y={k}x. Costruisci tre coppie (x,y), descrivi a parole la relazione e spiega quale caratteristica avrebbe il grafico rispetto all'origine.",band,support,params={"k":k},dimensions=["representation","reasoning","explanation"],acceptable=f"rapporto y/x={k}; grafico lineare passante per l'origine")
    return task(task_id,"math.y3.multirep.table",f"Se y={k}x e x={x}, quanto vale y?",str(y),band,support,params={"k":k,"x":x},dimensions=["accuracy","representation"])


def function_families(phase, seed, band, support, task_id):
    r=_r(seed); k=r.randint(2,5); family=r.choice(["direct","inverse","square"])
    if family=="direct": formula=f"y={k}x"; invariant=f"y/x={k}"
    elif family=="inverse": formula=f"y={k*6}/x"; invariant=f"x·y={k*6}"
    else: formula=f"y={k}x²"; invariant="il valore cresce con il quadrato di x"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"math.y3.function-family.identify",f"Considera {formula}. Descrivi la famiglia di relazione, indica una proprietà/invariante utile e spiega come distinguerla da una semplice relazione crescente.",band,support,params={"family":family,"k":k},dimensions=["conceptual_understanding","representation","explanation"],acceptable=invariant)
    return task(task_id,"math.y3.function-family.classify",f"La formula {formula} rappresenta una relazione diretta, inversa o quadratica?",{"direct":"diretta","inverse":"inversa","square":"quadratica"}[family],band,support,params={"family":family,"k":k},dimensions=["accuracy","conceptual_understanding"])


MATH_Y3_NUMBERS_ALGEBRA_BUILDERS={
    "math.numbers.signed-number-sense":signed_number_sense,
    "math.numbers.signed-operations":signed_operations,
    "math.numbers.rational-expressions":rational_expressions,
    "math.numbers.real-number-system":real_number_system,
    "math.relations.symbolic-generalization":symbolic_generalization,
    "math.relations.algebraic-expressions":algebraic_expressions,
    "math.relations.first-degree-equations":first_degree_equations,
    "math.relations.multiple-representations":multiple_representations,
    "math.relations.function-families":function_families,
}
