from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def _lexis(phase,seed,band,support,task_id,topic,words,family):
    r=_r(seed); word=r.choice(words)
    if phase_mode(phase)=="transfer":
        return open_task(task_id,f"eng.y2.lexis.{family}.use",f"Use the word '{word}' in a realistic {topic} situation, then add a second sentence that gives useful contextual information.",band,support,params={"word":word,"topic":topic},dimensions=["vocabulary","meaning","production"],acceptable="word used with a meaning and collocation coherent with the topic")
    return task(task_id,f"eng.y2.lexis.{family}.recognise",f"Which topic best matches the word '{word}': {topic} or an unrelated school subject?",topic,band,support,params={"word":word,"topic":topic},dimensions=["accuracy","vocabulary"])

def travel(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"travel and holidays",["platform","luggage","departure","hotel","journey","ticket"],"travel")
def shopping(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"shopping, clothes and money",["size","price","change","receipt","jacket","cash"],"shopping")
def health(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"health and the body",["headache","stomach ache","temperature","ankle","medicine","rest"],"health")
def environment(phase,seed,band,support,task_id): return _lexis(phase,seed,band,support,task_id,"places and the environment",["forest","river","traffic","pollution","coast","recycling"],"environment")

def past_ed(phase,seed,band,support,task_id):
    r=_r(seed); word,sound=r.choice([("worked","/t/"),("played","/d/"),("wanted","/ɪd/"),("visited","/ɪd/")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.phonology.ed.explain",f"Say or mark the ending sound in '{word}' and explain why pronouncing every -ed as a separate /ed/ syllable would reduce naturalness.",band,support,params={"word":word,"sound":sound},dimensions=["phonology","explanation"],acceptable=f"target ending {sound}")
    return task(task_id,"eng.y2.phonology.ed.identify",f"Which -ed ending does '{word}' have: /t/, /d/ or /ɪd/?",sound,band,support,params={"word":word},dimensions=["accuracy","phonology"])

def sentence_stress(phase,seed,band,support,task_id):
    r=_r(seed); sentence=r.choice(["I bought a NEW jacket yesterday.","The TRAIN leaves at NINE.","We VISITED London last WEEK."])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.phonology.sentence-stress",f"Read or mark the information words that deserve strongest stress in: {sentence} Explain how this helps a listener find the key message.",band,support,params={"sentence":sentence},dimensions=["phonology","listening_strategy","explanation"],acceptable="content/information words receive prominence")
    return open_task(task_id,"eng.y2.phonology.keywords",f"Underline or list the two most informative words in: {sentence}",band,support,params={"sentence":sentence},dimensions=["phonology","gist"],acceptable="selects the main content words")

def reading_multitext(phase,seed,band,support,task_id):
    r=_r(seed); need=r.choice(["a cheap train after 5 pm","a shop with sports clothes","a quiet place near nature"]); options=["A: City Store - fashion and trainers, open until 8.","B: Green Park Hostel - outside town, quiet rooms.","C: Rail offer - evening trains from 17:30 at reduced price."]; correct={"a cheap train after 5 pm":"C","a shop with sports clothes":"A","a quiet place near nature":"B"}[need]
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.reading.multitext.reason",f"A person needs {need}. Read: {' | '.join(options)} Choose the best option and justify your choice using two details, not just one matching word.",band,support,params={"need":need},dimensions=["reading","evidence_use","explanation"],acceptable=correct)
    return task(task_id,"eng.y2.reading.multitext.match",f"Need: {need}. Options: {' | '.join(options)} Which option fits best?",correct,band,support,params={"need":need},dimensions=["accuracy","reading"])

def reading_narrative(phase,seed,band,support,task_id):
    r=_r(seed); name=r.choice(["Maya","Tom","Leo","Sara"]); text=f"{name} missed the early bus, so they walked to the station. There they met a friend and caught the next train. They arrived late but still joined the museum tour."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.reading.narrative.sequence",f"Read: {text} Retell the three main events in order and explain which word shows a consequence.",band,support,params={"name":name},dimensions=["reading","sequencing","explanation"],acceptable="missed bus -> station/friend/train -> museum; 'so' signals consequence")
    return task(task_id,"eng.y2.reading.narrative.detail",f"Read: {text} Why did {name} walk to the station?","because they missed the early bus",band,support,params={"name":name},dimensions=["accuracy","reading"])

def listening_announcements(phase,seed,band,support,task_id):
    r=_r(seed); time=r.choice(["9:20","10:45","14:30"]); platform=r.choice(["2","4","6"]); script=f"Attention please. The train to Oxford leaves at {time} from platform {platform}."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.listening.announcement.notes",f"Listen to the tutor reading the announcement. Write only the destination, time and platform as short notes.",band,support,params={"time":time,"platform":platform},dimensions=["listening","note_taking","detail"],acceptable=f"Oxford; {time}; platform {platform}",rubric={"full_credit":"Captures all three practical details without a full transcription."},errors=[{"pattern":"transcribes_everything","code":"strategy_error"}])
    return task(task_id,"eng.y2.listening.announcement.detail","Listen to the tutor reading the announcement. Which platform does the train leave from?",platform,band,support,params={"time":time,"platform":platform,"tutor_script":script},dimensions=["accuracy","listening","detail"],extra_solution={"tutor_script":script})

def listening_narrative(phase,seed,band,support,task_id):
    r=_r(seed); place=r.choice(["the beach","a science museum","a football match"]); script=f"Last Saturday, Ben went to {place} with his cousin. They arrived in the morning, had lunch nearby and came home at six. Ben said the best part was being together."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y2.listening.narrative.sequence","Listen to the tutor reading a short past experience. Note the place, two events in order and the speaker's final opinion.",band,support,params={"place":place},dimensions=["listening","sequencing","gist_detail"],acceptable=f"{place}; arrival/lunch/home in order; best part being together",rubric={"full_credit":"Captures main setting, sequence and final evaluation."})
    return task(task_id,"eng.y2.listening.narrative.gist","Listen to the tutor reading the story. Where did Ben go?",place,band,support,params={"place":place,"tutor_script":script},dimensions=["accuracy","listening"],extra_solution={"tutor_script":script})


ENGLISH_Y2_RECEPTIVE_BUILDERS={
    "eng.vocabulary.travel_holidays":travel,
    "eng.vocabulary.shopping_clothes_money":shopping,
    "eng.vocabulary.health_body":health,
    "eng.vocabulary.places_environment":environment,
    "eng.phonology.past_ed_endings":past_ed,
    "eng.phonology.sentence_stress":sentence_stress,
    "eng.reading.everyday_multitext":reading_multitext,
    "eng.reading.simple_narratives_biographies":reading_narrative,
    "eng.listening.announcements_directions":listening_announcements,
    "eng.listening.simple_narratives":listening_narrative,
}
