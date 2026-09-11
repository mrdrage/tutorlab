from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)

def _open(task_id,family,prompt,band,support,params,dimensions,acceptable):
    return open_task(task_id,family,prompt,band,support,params=params,dimensions=dimensions,acceptable=acceptable,rubric={"full_credit":acceptable})

def shopping_services(phase,seed,band,support,task_id):
    r=_r(seed); item=r.choice(["a jacket","trainers","a backpack","a T-shirt"]); detail=r.choice(["size M","under £30","blue","a different size"])
    return _open(task_id,"eng.y2.interaction.shopping",f"Role-play a shop exchange. Ask for {item} with this requirement: {detail}. Include price or size, react to the answer and close the transaction politely.",band,support,{"item":item,"detail":detail},["interaction","vocabulary","functional_language"],"Completes a multi-turn transaction with an appropriate request, response and follow-up.")

def travel_directions(phase,seed,band,support,task_id):
    r=_r(seed); destination=r.choice(["the station","the museum","the bus stop","the hotel"])
    return _open(task_id,"eng.y2.interaction.directions",f"Role-play asking for and giving directions to {destination}. Include at least two spatial instructions and one clarification question.",band,support,{"destination":destination},["interaction","vocabulary","repair_strategy"],"Directions are understandable and the exchange includes a clarification move.")

def invitations(phase,seed,band,support,task_id):
    r=_r(seed); activity=r.choice(["go to the cinema","play basketball","visit the market","have lunch"]); day=r.choice(["Friday","Saturday","Sunday"])
    return _open(task_id,"eng.y2.interaction.arrangements",f"Create a short dialogue to arrange to {activity} on {day}. Include an invitation, one scheduling problem, a counterproposal and a final agreement.",band,support,{"activity":activity,"day":day},["interaction","future_reference","negotiation"],"Negotiates time/place and reaches a clear agreement using appropriate future language.")

def health_advice(phase,seed,band,support,task_id):
    r=_r(seed); problem=r.choice(["a headache","a sore throat","a stomach ache","feeling very tired"])
    return _open(task_id,"eng.y2.interaction.health",f"Role-play a conversation about {problem}. The helper asks one useful question and gives a relevant should/shouldn't recommendation.",band,support,{"problem":problem},["interaction","vocabulary","advice"],"Problem is described clearly; advice is relevant and at least one clarification question is used.")

def past_event(phase,seed,band,support,task_id):
    r=_r(seed); setting=r.choice(["a school trip","a family day out","a match","a weekend visit"])
    return _open(task_id,"eng.y2.production.past-event",f"Tell a short story about {setting}. Include where/when, at least three events in order, one irregular past verb and a final reaction.",band,support,{"setting":setting},["spoken_production","past_reference","cohesion"],"Produces a comprehensible past sequence with temporal order and a closing reaction.")

def compare_plans(phase,seed,band,support,task_id):
    r=_r(seed); a,b=r.choice([("the mountains","the seaside"),("train","bus"),("city break","camping")])
    return _open(task_id,"eng.y2.production.compare-plans",f"Compare {a} and {b}, say which you prefer, give at least two comparison points and describe one plan using going to.",band,support,{"a":a,"b":b},["spoken_production","comparison","future_reference"],"Connects comparison, preference and a simple future plan with reasons.")

def informal_email(phase,seed,band,support,task_id):
    r=_r(seed); purpose=r.choice(["invite a friend for the weekend","describe holiday plans","reply to a friend's invitation"])
    return _open(task_id,"eng.y2.writing.email",f"Write a short informal email to {purpose}. Include greeting, 3 content points, one question to the reader and a closing.",band,support,{"purpose":purpose},["writing","task_completion","cohesion"],"Covers all requested points with a recognisable informal email structure and simple linking.")

def simple_narrative(phase,seed,band,support,task_id):
    r=_r(seed); trigger=r.choice(["you missed a bus","you found a lost phone","it started raining","you met an old friend"])
    return _open(task_id,"eng.y2.writing.narrative",f"Write a short past narrative beginning from this event: {trigger}. Use a clear sequence, at least two past verbs and one time connector.",band,support,{"trigger":trigger},["writing","past_reference","cohesion"],"Events are ordered and understandable, with consistent past reference and basic connectors.")

def summarise_points(phase,seed,band,support,task_id):
    r=_r(seed); message=r.choice(["The sports centre opens at 9, the pool is closed today, and basketball starts at 4.","The train is delayed 20 minutes, platform 5 is unchanged, and tickets remain valid."])
    return _open(task_id,"eng.y2.mediation.summary",f"Read this message: '{message}' A friend only needs the essential practical information. Relay the 2-3 key points without copying the whole message.",band,support,{"message":message},["mediation","selection","clarity"],"Selects the essential information and relays it clearly for the recipient's purpose.")

def collaborative_task(phase,seed,band,support,task_id):
    r=_r(seed); task_name=r.choice(["choose a class trip","plan a small party","choose an after-school activity"])
    return _open(task_id,"eng.y2.mediation.collaboration",f"In a group task to {task_name}, contribute a proposal, respond to another idea, reformulate one point if needed and help the group reach a choice.",band,support,{"task":task_name},["mediation","interaction","collaboration"],"Builds on another contribution and helps move the group toward a shared decision.")

def gist_detail_notes(phase,seed,band,support,task_id):
    r=_r(seed); text=r.choice(["A school notice gives a trip date, price, meeting point and return time.","A travel announcement gives destination, departure time, platform and delay."])
    if phase_mode(phase)=="transfer":
        return _open(task_id,"eng.y2.strategy.gist-detail",f"For this task type: {text} Explain how your reading/listening strategy changes if the question asks for the general purpose versus one exact time or number. Give a sample note format.",band,support,{"text":text},["learning_strategy","explanation","note_taking"],"Distinguishes gist from detail search and proposes concise keyword notes.")
    return task(task_id,"eng.y2.strategy.choose","If the question asks only 'What is this message mainly about?', should you first use gist reading/listening or detailed transcription?","gist",band,support,params={"text":text},dimensions=["accuracy","learning_strategy"])

def intercultural_lifestyles(phase,seed,band,support,task_id):
    r=_r(seed); topic=r.choice(["school timetable","meal times","weekend activities","public transport habits"])
    return _open(task_id,"eng.y2.intercultural.compare",f"Compare one example of {topic} in two contexts. Use cautious language such as 'in this example' or 'some people', give one similarity and one difference, and avoid broad generalisations.",band,support,{"topic":topic},["intercultural","comparison","language_awareness"],"Describes similarity and difference using evidence-limited, non-absolute language.")


ENGLISH_Y2_PRODUCTIVE_BUILDERS={
    "eng.interaction.shopping_services":shopping_services,
    "eng.interaction.travel_directions":travel_directions,
    "eng.interaction.invitations_arrangements":invitations,
    "eng.interaction.health_advice":health_advice,
    "eng.production.past_event":past_event,
    "eng.production.compare_plans":compare_plans,
    "eng.writing.informal_email":informal_email,
    "eng.writing.simple_narrative":simple_narrative,
    "eng.mediation.summarise_simple_points":summarise_points,
    "eng.mediation.collaborative_task":collaborative_task,
    "eng.learning.gist_detail_notes":gist_detail_notes,
    "eng.intercultural.compare_lifestyles":intercultural_lifestyles,
}
