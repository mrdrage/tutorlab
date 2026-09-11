from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def be_task(phase,seed,band,support,task_id):
    r=random.Random(seed); subj,form=r.choice([("I","am"),("you","are"),("he","is"),("she","is"),("we","are"),("they","are")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.be.transfer",f"Write one question and one answer with {subj} and the verb be.",band,support,params={"subject":subj},dimensions=["accuracy","interaction","transfer"],acceptable="correct form of be and coherent exchange")
    return task(task_id,"eng.y1.be.form",f"Complete: {subj} ___ ready.",form,band,support,params={"subject":subj},dimensions=["accuracy","grammar_control"])


def have_got_task(phase,seed,band,support,task_id):
    r=random.Random(seed); subj,form=r.choice([("I","have"),("you","have"),("he","has"),("she","has"),("we","have"),("they","have")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.have-got.transfer",f"Write one possession question and short answer using {subj} and have got.",band,support,params={"subject":subj},dimensions=["accuracy","interaction","transfer"],acceptable="correct have/has got question and answer")
    return task(task_id,"eng.y1.have-got.form",f"Complete: {subj} ___ got a book.",form,band,support,params={"subject":subj},dimensions=["accuracy","grammar_control"])


def nominal_basics_task(phase,seed,band,support,task_id):
    r=random.Random(seed); word=r.choice(["apple","orange","umbrella","book","teacher"]); article="an" if word[0] in "aeiou" else "a"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.nominal.transfer",f"Use '{word}' once in the singular with the correct article and once in the plural.",band,support,params={"word":word},dimensions=["accuracy","transfer"],acceptable=f"{article} {word} plus correct plural")
    return task(task_id,"eng.y1.nominal.article",f"Choose the article: ___ {word}.",article,band,support,params={"word":word},dimensions=["accuracy","grammar_control"])


def possessives_task(phase,seed,band,support,task_id):
    r=random.Random(seed); owner,poss=r.choice([("Marco","his"),("Anna","her"),("I","my"),("we","our"),("they","their")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.possessives.transfer",f"Write a sentence about a school bag owned by {owner}, using the correct possessive form.",band,support,params={"owner":owner},dimensions=["accuracy","transfer"],acceptable=f"appropriate possessive such as {poss}")
    return task(task_id,"eng.y1.possessives.choose",f"Complete: {owner} has a bike. ___ bike is blue.",poss,band,support,params={"owner":owner},dimensions=["accuracy","grammar_control"])


GRAMMAR_CORE_BUILDERS={
    "eng.grammar.be":be_task,
    "eng.grammar.have_got":have_got_task,
    "eng.grammar.nominal_basics":nominal_basics_task,
    "eng.grammar.possessives":possessives_task,
}
