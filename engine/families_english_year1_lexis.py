from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task

DOMAINS={
    "eng.vocabulary.personal_family":[("mother","family"),("brother","family"),("friendly","description"),("tall","description")],
    "eng.vocabulary.school_routines":[("maths","school subject"),("pencil","school object"),("breakfast","daily routine"),("homework","daily routine")],
    "eng.vocabulary.home_town":[("kitchen","home"),("bedroom","home"),("library","town"),("station","town")],
    "eng.vocabulary.free_time_food":[("football","free time"),("reading","free time"),("pasta","food"),("apple","food")],
}


def vocabulary_task(competency_id,phase,seed,band,support,task_id):
    r=random.Random(seed); word,category=r.choice(DOMAINS[competency_id])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.vocabulary.transfer",f"Use the word '{word}' in a short meaningful sentence connected to {category}.",band,support,params={"word":word,"category":category},dimensions=["lexical_range","accuracy","transfer"],acceptable="sentence uses the target word with the intended meaning")
    return task(task_id,"eng.y1.vocabulary.category",f"Which category best matches '{word}'?",category,band,support,params={"word":word},dimensions=["accuracy","lexical_control"])


def alphabet_spelling(phase,seed,band,support,task_id):
    r=random.Random(seed); word=r.choice(["book","school","friend","orange","house"]); spelling="-".join(word.upper())
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.spelling.transfer",f"Spell the word '{word}' aloud or in writing, then explain which letters could be easily confused when listening.",band,support,params={"word":word},dimensions=["phonological_control","explanation"],acceptable=spelling)
    return task(task_id,"eng.y1.spelling.sequence",f"Write the spelling of '{word}' using capital letters separated by hyphens.",spelling,band,support,params={"word":word},dimensions=["accuracy","phonological_control"])


def word_stress(phase,seed,band,support,task_id):
    r=random.Random(seed); word,stress=r.choice([("teacher","TEA-cher"),("computer","com-PU-ter"),("banana","ba-NA-na"),("family","FAM-i-ly")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.word-stress.transfer",f"Say or mark the stress in '{word}', then use the word in a short sentence while keeping the stress recognizable.",band,support,params={"word":word},dimensions=["phonological_control","transfer"],acceptable=stress)
    return task(task_id,"eng.y1.word-stress.mark",f"Which syllable is stressed in '{word}'? Write the pattern with the stressed syllable in capitals.",stress,band,support,params={"word":word},dimensions=["accuracy","phonological_control"])


def make_vocab_builder(competency_id):
    return lambda phase,seed,band,support,task_id: vocabulary_task(competency_id,phase,seed,band,support,task_id)


LEXIS_BUILDERS={key:make_vocab_builder(key) for key in DOMAINS}
LEXIS_BUILDERS.update({
    "eng.phonology.alphabet_spelling":alphabet_spelling,
    "eng.phonology.basic_word_stress":word_stress,
})
