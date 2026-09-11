from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def present_perfect_experience(phase,seed,band,support,task_id):
    r=_r(seed); person=r.choice(["Maya","Tom","Leo"]); activity=r.choice(["visit London","try sushi","fly on a plane"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.pp.experience",f"Ask {person} whether they have ever {activity}, then add one follow-up question that asks for a dated past detail. Explain why the two questions need different tenses.",band,support,params={"person":person,"activity":activity},dimensions=["grammar","interaction","explanation"],acceptable="Present Perfect for experience; Past Simple for dated detail")
    return task(task_id,"eng.y3.pp.form",f"Complete with Present Perfect: {person} ___ never ___ (visit) London.","has never visited",band,support,params={"person":person},dimensions=["accuracy","grammar"])

def present_perfect_vs_past(phase,seed,band,support,task_id):
    r=_r(seed); marker=r.choice(["last year","yesterday","in 2024"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.pp-vs-past.contrast",f"Write two connected questions about travel: one with 'Have you ever...?' and one asking when/where the event happened. Explain how the time reference changes the tense.",band,support,params={"marker":marker},dimensions=["grammar","meaning","explanation"],acceptable="experience with Present Perfect; dated event with Past Simple")
    return task(task_id,"eng.y3.pp-vs-past.choose",f"Choose the correct tense: I ___ to Rome {marker}. (go)","went",band,support,params={"marker":marker},dimensions=["accuracy","grammar"])

def will_future(phase,seed,band,support,task_id):
    r=_r(seed); situation=r.choice(["The phone is ringing.","I think cities will be greener.","This bag is heavy."])
    answer={"The phone is ringing.":"I'll answer it.","I think cities will be greener.":"prediction","This bag is heavy.":"I'll help you."}[situation]
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.will.function",f"Situation: {situation} Produce a natural sentence with will and explain whether it is a prediction, instant decision, offer or promise.",band,support,params={"situation":situation},dimensions=["grammar","meaning","production"],acceptable="appropriate use of will for the communicative function")
    return task(task_id,"eng.y3.will.recognise",f"In '{situation}' which is the most likely function of will: prediction, instant decision/offer, or fixed arrangement?",("prediction" if "think" in situation else "instant decision/offer"),band,support,params={"situation":situation},dimensions=["accuracy","meaning"])

def first_conditional(phase,seed,band,support,task_id):
    r=_r(seed); condition=r.choice(["it rains","we finish early","you study regularly"]); result=r.choice(["we'll stay inside","we'll go for a walk","you'll improve"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.first-conditional.logic",f"Create a logical first conditional using the idea '{condition}' and a realistic consequence. Then rewrite it with the result clause first without changing the meaning.",band,support,params={"condition":condition},dimensions=["grammar","logic","production"],acceptable="if + Present Simple, will + base verb; logical consequence")
    return task(task_id,"eng.y3.first-conditional.complete",f"Complete: If {condition}, {result.replace("we'll","we ___").replace("you'll","you ___")}","will",band,support,params={"condition":condition,"result":result},dimensions=["accuracy","grammar"])

def may_might(phase,seed,band,support,task_id):
    r=_r(seed); event=r.choice(["rain tomorrow","be late","visit us this weekend"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.may-might.degree",f"Express uncertainty about '{event}' using may or might, then contrast it with a more direct prediction using will. Explain the difference in certainty.",band,support,params={"event":event},dimensions=["grammar","meaning","explanation"],acceptable="may/might expresses possibility; will is more direct prediction")
    return task(task_id,"eng.y3.may-might.form",f"Complete with a modal of possibility: It ___ {event}.","may/might",band,support,params={"event":event},dimensions=["accuracy","grammar"])

def relative_clauses(phase,seed,band,support,task_id):
    r=_r(seed); antecedent=r.choice([("a doctor","who"),("a device","which"),("a book","that")]); noun,rel=antecedent
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.relative.combine",f"Combine two short sentences into one relative clause about {noun}. Explain why you chose who, which or that.",band,support,params={"noun":noun,"rel":rel},dimensions=["grammar","cohesion","explanation"],acceptable=f"relative clause with {rel} or another valid choice")
    return task(task_id,"eng.y3.relative.choose",f"Choose a relative pronoun: {noun} is something/someone ___ can help in this context.",rel,band,support,params={"noun":noun},dimensions=["accuracy","grammar"])

def passive_basic(phase,seed,band,support,task_id):
    r=_r(seed); object_,verb,participle=r.choice([("English","speak","spoken"),("This phone","make","made"),("The bridge","build","built")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.passive.focus",f"Write a simple passive sentence about '{object_}' using '{participle}' and explain why the result/action is more important than the agent in your sentence.",band,support,params={"object":object_,"verb":verb},dimensions=["grammar","meaning","explanation"],acceptable="be + past participle with appropriate subject focus")
    return task(task_id,"eng.y3.passive.form",f"Complete the passive: {object_} is ___ ({verb}).",participle,band,support,params={"object":object_,"verb":verb},dimensions=["accuracy","grammar"])

def reported_speech(phase,seed,band,support,task_id):
    r=_r(seed); quote=r.choice(["I am tired","I like this film","I went home early"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.reported.relay",f"A classmate says: '{quote}'. Report the essential message to another person without copying it word for word. Keep pronouns and time reference coherent.",band,support,params={"quote":quote},dimensions=["grammar","mediation","meaning"],acceptable="simple coherent reported message preserving meaning")
    return open_task(task_id,"eng.y3.reported.basic",f"Report this message simply: '{quote}'.",band,support,params={"quote":quote},dimensions=["grammar","meaning"],acceptable="reported content with coherent pronoun/tense choices")

def connectors(phase,seed,band,support,task_id):
    r=_r(seed); relation=r.choice([("cause","because"),("result","so"),("contrast","but"),("sequence","then")]); kind,conn=relation
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.connectors.cohesion",f"Write a short four-sentence paragraph that includes a clear cause, result, contrast and sequence. Use suitable connectors and explain one choice.",band,support,params={"focus":kind},dimensions=["cohesion","grammar","writing"],acceptable="logical use of because/so/but/sequence connectors")
    return task(task_id,"eng.y3.connectors.choose",f"Which connector best signals {kind}: because, so, but or then?",conn,band,support,params={"relation":kind},dimensions=["accuracy","cohesion"])

ENGLISH_Y3_GRAMMAR_BUILDERS={
    "eng.grammar.present_perfect_experience":present_perfect_experience,
    "eng.grammar.present_perfect_vs_past":present_perfect_vs_past,
    "eng.grammar.will_future":will_future,
    "eng.grammar.first_conditional":first_conditional,
    "eng.grammar.may_might":may_might,
    "eng.grammar.relative_clauses_basic":relative_clauses,
    "eng.grammar.passive_basic":passive_basic,
    "eng.grammar.reported_speech_basic":reported_speech,
    "eng.grammar.connectors_cohesion":connectors,
}
