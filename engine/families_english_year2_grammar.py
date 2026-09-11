from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)

def past_be(phase,seed,band,support,task_id):
    r=_r(seed); subject=r.choice(["I","she","they","we"]); place=r.choice(["at home","at school","in Rome","at the park"]); form="was" if subject in {"I","she"} else "were"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.past-be.use",f"Write two connected sentences about yesterday using {subject} and the verb be, one affirmative and one negative.",band,support,params={"subject":subject,"place":place},dimensions=["accuracy","production","transfer"],acceptable="correct use of was/were and wasn't/weren't")
    return task(task_id,"eng.y2.past-be.form",f"Complete: Yesterday {subject} ___ {place}.",form,band,support,params={"subject":subject,"place":place},dimensions=["accuracy","grammar"])

def past_regular(phase,seed,band,support,task_id):
    r=_r(seed); verb=r.choice(["play","visit","watch","clean"]); subject=r.choice(["I","we","they"]); past=verb+"ed" if not verb.endswith("e") else verb+"d"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.past-regular.narrate",f"Write a short three-event sequence about last weekend. Include the verb {verb} and at least one negative sentence with didn't.",band,support,params={"verb":verb},dimensions=["grammar","cohesion","production"],acceptable="past time reference, regular past form, base form after didn't")
    return task(task_id,"eng.y2.past-regular.form",f"Complete: Last Saturday {subject} ___ ({verb}) together.",past,band,support,params={"subject":subject,"verb":verb},dimensions=["accuracy","grammar"])

def past_irregular(phase,seed,band,support,task_id):
    r=_r(seed); pairs=[("go","went"),("see","saw"),("have","had"),("buy","bought"),("take","took")]; verb,past=r.choice(pairs)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.past-irregular.use",f"Tell a short past event using {past} naturally, then ask one question about the event with did.",band,support,params={"verb":verb,"past":past},dimensions=["grammar","interaction","production"],acceptable="irregular form in affirmative and base form after did")
    return task(task_id,"eng.y2.past-irregular.form",f"Complete: Yesterday I ___ ({verb}) something interesting.",past,band,support,params={"verb":verb},dimensions=["accuracy","grammar"])

def comparatives(phase,seed,band,support,task_id):
    r=_r(seed); adj,comp,sup=r.choice([("tall","taller","the tallest"),("fast","faster","the fastest"),("good","better","the best"),("interesting","more interesting","the most interesting")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.comparison.choice",f"Compare two places or activities using {adj}, then make a superlative statement about three options. Explain the difference in meaning between the two forms.",band,support,params={"adj":adj},dimensions=["grammar","meaning","production"],acceptable=f"correct use of {comp} and {sup}")
    return task(task_id,"eng.y2.comparison.form",f"Complete the comparative of '{adj}'.",comp,band,support,params={"adj":adj},dimensions=["accuracy","grammar"])

def quantifiers(phase,seed,band,support,task_id):
    r=_r(seed); noun,countable=r.choice([("apples",True),("books",True),("water",False),("rice",False)]); answer="many" if countable else "much"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.quantifiers.transaction",f"You are preparing a shopping list. Write one question with how much and one with how many, then add a sentence with a little or a few.",band,support,params={"noun":noun},dimensions=["grammar","function","production"],acceptable="countable/uncountable distinction is maintained")
    return task(task_id,"eng.y2.quantifiers.choose",f"Complete: How ___ {noun} do we need?",answer,band,support,params={"noun":noun,"countable":countable},dimensions=["accuracy","grammar"])

def must_have_to(phase,seed,band,support,task_id):
    r=_r(seed); scenario=r.choice(["wear a seat belt","bring a ticket","finish homework","enter this room"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.obligation.meaning",f"Write one rule with must or have to about '{scenario}', one prohibition with mustn't, and one sentence showing no necessity with don't have to. Make the meanings clearly different.",band,support,params={"scenario":scenario},dimensions=["grammar","meaning","transfer"],acceptable="distinguishes obligation, prohibition and lack of necessity")
    return task(task_id,"eng.y2.obligation.choice","Which means 'it is not necessary': mustn't or don't have to?","don't have to",band,support,params={"scenario":scenario},dimensions=["accuracy","meaning"])

def should(phase,seed,band,support,task_id):
    r=_r(seed); problem=r.choice(["I have a headache.","I'm tired.","I can't sleep well.","I'm late for school every day."])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.should.advice",f"A friend says: '{problem}' Give two relevant pieces of advice with should/shouldn't and explain briefly why one is useful.",band,support,params={"problem":problem},dimensions=["grammar","relevance","production"],acceptable="advice is grammatically correct and relevant to the problem")
    return task(task_id,"eng.y2.should.form","Complete the advice: You ___ drink more water.","should",band,support,params={"problem":problem},dimensions=["accuracy","grammar"])

def going_to(phase,seed,band,support,task_id):
    r=_r(seed); subject=r.choice(["I","she","we","they"]); activity=r.choice(["visit London","study tonight","play tennis","cook dinner"]); be="am" if subject=="I" else "is" if subject=="she" else "are"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.going-to.plan",f"Write a short exchange about weekend plans using be going to. Include one question and one answer with a reason.",band,support,params={"activity":activity},dimensions=["grammar","interaction","production"],acceptable="correct be going to structure used for plans")
    return task(task_id,"eng.y2.going-to.form",f"Complete: {subject} ___ going to {activity}.",be,band,support,params={"subject":subject,"activity":activity},dimensions=["accuracy","grammar"])

def present_cont_future(phase,seed,band,support,task_id):
    r=_r(seed); day=r.choice(["tomorrow","on Friday","next Saturday"]); activity=r.choice(["meeting Anna","taking the train","playing football","having dinner with Luca"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.pc-future.arrangement",f"Write two sentences: one about an arrangement already fixed for {day}, and one about something happening now. Use Present Continuous in both but make the time reference unmistakable.",band,support,params={"day":day,"activity":activity},dimensions=["grammar","meaning","transfer"],acceptable="future arrangement and current action are distinguished by context")
    return task(task_id,"eng.y2.pc-future.recognise",f"In 'I'm {activity} {day}', does the Present Continuous refer to now or to a future arrangement?","future arrangement",band,support,params={"day":day,"activity":activity},dimensions=["accuracy","meaning"])

def would_like(phase,seed,band,support,task_id):
    r=_r(seed); item=r.choice(["a sandwich","a ticket","some water","a blue T-shirt"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.would-like.service",f"Write a short customer-assistant exchange using I'd like and Would you like while ordering or buying {item}.",band,support,params={"item":item},dimensions=["grammar","interaction","register"],acceptable="polite request/offering structure used appropriately")
    return task(task_id,"eng.y2.would-like.form",f"Complete politely: I ___ {item}, please.","would like",band,support,params={"item":item},dimensions=["accuracy","grammar"])


ENGLISH_Y2_GRAMMAR_BUILDERS={
    "eng.grammar.past_be":past_be,
    "eng.grammar.past_regular":past_regular,
    "eng.grammar.past_irregular":past_irregular,
    "eng.grammar.comparatives_superlatives":comparatives,
    "eng.grammar.quantifiers":quantifiers,
    "eng.grammar.must_have_to":must_have_to,
    "eng.grammar.should":should,
    "eng.grammar.going_to":going_to,
    "eng.grammar.present_continuous_future":present_cont_future,
    "eng.grammar.would_like":would_like,
}
