from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def _lexis(phase,seed,band,support,task_id,topic,words,family):
    r=_r(seed); word=r.choice(words)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,f"eng.y3.lexis.{family}.use",f"Use '{word}' in a realistic sentence about {topic}, then add a second sentence that shows why the word fits that context.",band,support,params={"word":word,"topic":topic},dimensions=["vocabulary","meaning","production"],acceptable="accurate use with a plausible collocation and context")
    return task(task_id,f"eng.y3.lexis.{family}.recognise",f"Which topic best matches '{word}': {topic} or an unrelated topic?",topic,band,support,params={"word":word},dimensions=["accuracy","vocabulary"])

def jobs(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"jobs, skills and future plans",["engineer","designer","apply","skill","career","training"],"jobs")
def technology(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"technology and digital media",["device","upload","privacy","account","screen time","message"],"technology")
def environment(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"environment and global issues",["waste","energy","climate","recycle","pollution","resource"],"environment")
def culture(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"culture, events and travel",["festival","exhibition","landmark","performance","guide","tradition"],"culture")
def emotions(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"emotions and relationships",["proud","worried","disappointed","supportive","confident","upset"],"emotions")

def connected_speech(phase,seed,band,support,task_id):
    r=_r(seed); phrase=r.choice(["What are you going to do?","Have you ever been there?","Could you help me?"])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.phonology.connected",f"Read or listen to '{phrase}'. Mark the words that carry the main information and explain why function words may sound weaker in connected speech.",band,support,params={"phrase":phrase},dimensions=["phonology","listening_strategy","explanation"],acceptable="content words remain prominent; function words may be reduced")
    return open_task(task_id,"eng.y3.phonology.connected-recognition",f"In the phrase '{phrase}', identify two content words that should remain easy to hear.",band,support,params={"phrase":phrase},dimensions=["phonology","gist"],acceptable="two plausible content words")

def intonation(phase,seed,band,support,task_id):
    r=_r(seed); utterance,attitude=r.choice([("Really?","interest/surprise"),("Are you coming?","question"),("I'm not sure.","uncertainty")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.phonology.intonation-use",f"Say or annotate '{utterance}' so that it clearly expresses {attitude}. Explain what would become less clear with a completely flat intonation.",band,support,params={"utterance":utterance,"attitude":attitude},dimensions=["phonology","pragmatics","explanation"],acceptable=f"intonation makes {attitude} recognisable")
    return task(task_id,"eng.y3.phonology.intonation-recognise",f"What communicative attitude is most likely in '{utterance}' when said with marked intonation?",attitude,band,support,params={"utterance":utterance},dimensions=["accuracy","pragmatics"])

ENGLISH_Y3_LEXIS_PHONOLOGY_BUILDERS={
    "eng.vocabulary.jobs_future":jobs,
    "eng.vocabulary.technology_media":technology,
    "eng.vocabulary.environment_global":environment,
    "eng.vocabulary.culture_travel":culture,
    "eng.vocabulary.emotions_relationships":emotions,
    "eng.phonology.connected_speech":connected_speech,
    "eng.phonology.intonation_attitude":intonation,
}
