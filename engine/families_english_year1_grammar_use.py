from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def questions_task(phase,seed,band,support,task_id):
    r=random.Random(seed); label,word=r.choice([("place","Where"),("time","When"),("person","Who"),("reason","Why")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.questions.transfer",f"Write a complete question that asks about a {label}.",band,support,params={"type":label},dimensions=["accuracy","interaction","transfer"],acceptable=f"question beginning with {word} and correct word order")
    return task(task_id,"eng.y1.questions.word",f"Which question word asks about a {label}?",word,band,support,params={"type":label},dimensions=["accuracy","grammar_control"])


def frequency_task(phase,seed,band,support,task_id):
    r=random.Random(seed); adv=r.choice(["always","usually","often","sometimes","never"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.frequency.transfer",f"Write a school-routine sentence using '{adv}' in the correct position.",band,support,params={"adverb":adv},dimensions=["accuracy","writing","transfer"],acceptable="Present Simple sentence with correct adverb position")
    return task(task_id,"eng.y1.frequency.use",f"Complete with the given adverb: I ___ do my homework after dinner. ({adv})",adv,band,support,params={"adverb":adv},dimensions=["accuracy","grammar_control"])


def can_task(phase,seed,band,support,task_id):
    r=random.Random(seed); verb=r.choice(["swim","dance","cook","draw","sing"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.can.transfer",f"Write a short question-answer exchange about ability using can and '{verb}'.",band,support,params={"verb":verb},dimensions=["accuracy","interaction","transfer"],acceptable="Can ...? with coherent answer")
    return task(task_id,"eng.y1.can.form",f"Complete: She can ___ . ({verb})",verb,band,support,params={"verb":verb},dimensions=["accuracy","grammar_control"])


def there_task(phase,seed,band,support,task_id):
    r=random.Random(seed); n=r.randint(1,5); noun=r.choice(["book","chair","window"]); form="are" if n!=1 else "is"; label=noun+("s" if n!=1 else "")
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.there.transfer","Describe a room with two sentences: one with there is and one with there are.",band,support,params={"case":"room"},dimensions=["accuracy","writing","transfer"],acceptable="one correct singular and one correct plural sentence")
    return task(task_id,"eng.y1.there.form",f"Complete: There ___ {n} {label}.",form,band,support,params={"n":n,"noun":noun},dimensions=["accuracy","grammar_control"])


def present_continuous_task(phase,seed,band,support,task_id):
    r=random.Random(seed); subj,be=r.choice([("I","am"),("he","is"),("she","is"),("we","are"),("they","are")]); verb=r.choice(["read","play","cook","study"]); ing=verb+"ing"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.present-continuous.transfer",f"Write two sentences with '{verb}': one routine and one action happening now.",band,support,params={"subject":subj,"verb":verb},dimensions=["accuracy","transfer","grammar_control"],acceptable="clear Present Simple versus Present Continuous contrast")
    return task(task_id,"eng.y1.present-continuous.form",f"Complete: {subj} ___ {ing} now.",be,band,support,params={"subject":subj,"verb":verb},dimensions=["accuracy","grammar_control"])


GRAMMAR_USE_BUILDERS={
    "eng.grammar.basic_questions":questions_task,
    "eng.grammar.frequency":frequency_task,
    "eng.grammar.can_basic":can_task,
    "eng.grammar.there_is_are":there_task,
    "eng.grammar.present_continuous":present_continuous_task,
}
