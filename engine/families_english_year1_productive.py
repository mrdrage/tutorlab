from __future__ import annotations

import random
from engine.generation_common import open_task


def introductions(phase,seed,band,support,task_id):
    return open_task(task_id,"eng.y1.interaction.introductions","Create a short four-turn exchange to introduce yourself and ask the other person one personal question.",band,support,params={"turns":4},dimensions=["interaction","accuracy","independence"],acceptable="greeting, self-introduction, one suitable question, coherent reply",rubric={"full_credit":"Maintains a simple reciprocal exchange with understandable grammar and at least one question."})


def routine_exchanges(phase,seed,band,support,task_id):
    r=random.Random(seed); topic=r.choice(["school routine","free time","food preference"])
    return open_task(task_id,"eng.y1.interaction.routines",f"Create a short exchange about {topic}. Include one follow-up question that reacts to the other speaker's answer.",band,support,params={"topic":topic},dimensions=["interaction","transfer","accuracy"],acceptable="reciprocal exchange with relevant follow-up",rubric={"full_credit":"Responds to the partner and asks a relevant follow-up rather than producing isolated memorised lines."})


def spoken_production(phase,seed,band,support,task_id):
    r=random.Random(seed); focus=r.choice(["your school day","your family","your free time"])
    return open_task(task_id,"eng.y1.production.short-talk",f"Give a short spoken description of {focus} in 4-6 simple sentences. Link ideas with basic connectors such as and, but or then.",band,support,params={"focus":focus},dimensions=["spoken_production","fluency","accuracy"],acceptable="4-6 comprehensible connected sentences",rubric={"full_credit":"Produces several connected, understandable sentences on the topic without relying on a complete script."})


def writing_message(phase,seed,band,support,task_id):
    r=random.Random(seed); purpose=r.choice(["invite a classmate to study","say what time an activity starts","thank a friend for help"])
    return open_task(task_id,"eng.y1.writing.message",f"Write a very short message to {purpose}. Include all essential information in 2-4 sentences.",band,support,params={"purpose":purpose},dimensions=["writing","accuracy","communicative_success"],acceptable="brief purposeful message containing essential information",rubric={"full_credit":"Message has a clear purpose, contains the required information and is understandable to the recipient."})


def writing_paragraph(phase,seed,band,support,task_id):
    r=random.Random(seed); topic=r.choice(["your daily routine","your family","your favourite free-time activities"])
    return open_task(task_id,"eng.y1.writing.paragraph",f"Write a short paragraph of 5-7 sentences about {topic}. Keep one clear topic and use at least two simple connectors.",band,support,params={"topic":topic},dimensions=["writing","coherence","accuracy","independence"],acceptable="coherent short paragraph with simple connectors",rubric={"full_credit":"Maintains the topic, links ideas in a sensible order and remains understandable despite minor errors."})


def repair_clarify(phase,seed,band,support,task_id):
    r=random.Random(seed); situation=r.choice(["you did not hear a word","you do not know how to spell a name","you did not understand an instruction"])
    return open_task(task_id,"eng.y1.learning.repair",f"In English, what could you say when {situation}? Give one useful repair phrase and show how the conversation can continue.",band,support,params={"situation":situation},dimensions=["learning_strategy","interaction","transfer"],acceptable="appropriate request for repetition, spelling or clarification",rubric={"full_credit":"Uses a suitable repair phrase and resumes the exchange rather than abandoning it."})


def intercultural_greetings(phase,seed,band,support,task_id):
    r=random.Random(seed); context=r.choice(["meeting a teacher","meeting a close friend","leaving a shop after asking for help"])
    return open_task(task_id,"eng.y1.intercultural.greetings",f"Choose an appropriate English greeting or courtesy expression for this context: {context}. Explain briefly why it fits the situation.",band,support,params={"context":context},dimensions=["intercultural_awareness","pragmatic_control","explanation"],acceptable="context-appropriate greeting or courtesy formula with non-stereotyped explanation",rubric={"full_credit":"Chooses a socially appropriate expression and explains the choice in relation to the situation."})


PRODUCTIVE_BUILDERS={
    "eng.interaction.introductions_personal_info":introductions,
    "eng.interaction.routine_exchanges":routine_exchanges,
    "eng.production.describe_self_routine":spoken_production,
    "eng.writing.forms_messages":writing_message,
    "eng.writing.personal_paragraph":writing_paragraph,
    "eng.learning.repair_clarify":repair_clarify,
    "eng.intercultural.greetings_daily_life":intercultural_greetings,
}
