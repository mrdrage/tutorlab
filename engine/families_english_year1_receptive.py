from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def reading_personal(phase,seed,band,support,task_id):
    r=random.Random(seed); age=r.randint(11,13); hobby=r.choice(["football","reading","music"]); city=r.choice(["Rome","Leeds","Dublin"])
    text=f"Alex is {age}. Alex lives in {city} and likes {hobby}."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.reading.personal.transfer",f"Read: '{text}' Summarise the two most important facts without copying the whole text.",band,support,params={"age":age,"hobby":hobby,"city":city},dimensions=["reading","mediation","transfer"],acceptable=f"two correct facts such as age {age}, city {city}, hobby {hobby}")
    return task(task_id,"eng.y1.reading.personal.detail",f"Read: '{text}' Where does Alex live?",city,band,support,params={"age":age,"hobby":hobby,"city":city},dimensions=["accuracy","reading"])


def reading_signs(phase,seed,band,support,task_id):
    r=random.Random(seed); sign,meaning=r.choice([("Library closes at 4 pm","You must go before 4 pm"),("No food in the classroom","Do not eat in the classroom"),("Bus 12: 8:15","The bus leaves at 8:15")])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.reading.functional.transfer",f"Read the notice: '{sign}'. Explain what action a student should take because of it.",band,support,params={"sign":sign},dimensions=["reading","transfer","explanation"],acceptable=meaning)
    return task(task_id,"eng.y1.reading.functional.meaning",f"Read: '{sign}'. What does it mean?",meaning,band,support,params={"sign":sign},dimensions=["accuracy","reading"])


def listening_personal(phase,seed,band,support,task_id):
    r=random.Random(seed); age=r.randint(11,13); city=r.choice(["Bristol","Madrid","Naples"]); script=f"Hi, I'm Sam. I'm {age} and I live in {city}."
    prompt="Listen to the tutor's short message. How old is Sam?"
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.listening.personal.transfer","Listen to the tutor's message and report the two key personal details you hear.",band,support,params={"script":script},dimensions=["listening","mediation","transfer"],acceptable=f"age {age}; city {city}",rubric={"full_credit":"Reports both key details from the spoken message without adding unsupported information."})
    return task(task_id,"eng.y1.listening.personal.detail",prompt,str(age),band,support,params={"script":script},dimensions=["accuracy","listening"],extra_solution={"tutor_script":script})


def listening_instructions(phase,seed,band,support,task_id):
    r=random.Random(seed); first,second=r.choice([("open your book","write the date"),("stand up","close the door"),("take a pencil","draw a circle")]); script=f"First, {first}. Then, {second}."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y1.listening.instructions.transfer","Listen to the tutor and reconstruct the sequence of two actions in order.",band,support,params={"script":script},dimensions=["listening","sequence","transfer"],acceptable=f"1) {first}; 2) {second}")
    return task(task_id,"eng.y1.listening.instructions.order","Listen to the tutor. What is the second action?",second,band,support,params={"script":script},dimensions=["accuracy","listening"],extra_solution={"tutor_script":script})


def mediation_simple(phase,seed,band,support,task_id):
    r=random.Random(seed); time=r.choice(["3:30","4:15","5:00"]); place=r.choice(["library","sports centre","school hall"]); message=f"The meeting is at {time} in the {place}."
    return open_task(task_id,"eng.y1.mediation.relay",f"Read: '{message}' A classmate asks only where and when the meeting is. Relay just the essential information.",band,support,params={"time":time,"place":place},dimensions=["mediation","selection","accuracy"],acceptable=f"{time}; {place}",rubric={"full_credit":"Selects and relays the requested time and place without unnecessary copying."})


RECEPTIVE_BUILDERS={
    "eng.reading.short_personal_texts":reading_personal,
    "eng.reading.signs_instructions":reading_signs,
    "eng.listening.personal_information":listening_personal,
    "eng.listening.everyday_instructions":listening_instructions,
    "eng.mediation.relay_simple_information":mediation_simple,
}
