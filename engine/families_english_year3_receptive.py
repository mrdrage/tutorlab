from __future__ import annotations

import random
from engine.generation_common import open_task, phase_mode, task


def _r(seed): return random.Random(seed)


def reading_everyday(phase,seed,band,support,task_id):
    r=_r(seed); text=r.choice([
        "Library notice: The study room closes at 6 pm today, but books can be returned at the front desk until 7.",
        "Message: I'm at the sports centre. The swimming lesson starts at 5:30, so meet me near reception at 5:15."])
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.reading.everyday.evidence",f"Read: {text} State the main purpose and one specific detail. Then identify one conclusion that would NOT be justified by the text.",band,support,params={"text":text},dimensions=["reading","gist","evidence_use","inference"],acceptable="main purpose + accurate detail + unsupported inference identified")
    return task(task_id,"eng.y3.reading.everyday.gist",f"Read: {text} Is the text mainly giving practical information, telling a story, or expressing a long opinion?","practical information",band,support,params={"text":text},dimensions=["accuracy","reading","gist"])

def reading_article(phase,seed,band,support,task_id):
    r=_r(seed); topic=r.choice(["a young inventor","a school eco-project","a local athlete"]); text=f"An article describes {topic}. It explains how the project started, one difficulty, and the result. The writer says the experience changed the person's plans for the future."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.reading.article.summary",f"Read: {text} Summarise the main point in two sentences and separate it from one supporting detail.",band,support,params={"topic":topic},dimensions=["reading","cohesion","summarising"],acceptable="main idea distinguished from supporting detail")
    return task(task_id,"eng.y3.reading.article.main",f"Read: {text} What is the article mainly about?",f"the development and effect of {topic}",band,support,params={"topic":topic},dimensions=["accuracy","reading","gist"])

def reading_instructions(phase,seed,band,support,task_id):
    steps=["Switch off the device.","Disconnect the cable.","Wait ten seconds.","Reconnect it and restart."]
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.reading.instructions.order",f"Instructions: {' '.join(steps)} Explain why the order matters and identify what could go wrong if the second step were skipped.",band,support,params={"steps":steps},dimensions=["reading","sequencing","reasoning"],acceptable="procedure reconstructed in order; skipped step recognised as relevant")
    return task(task_id,"eng.y3.reading.instructions.detail",f"Instructions: {' '.join(steps)} What should you do immediately after switching off the device?","Disconnect the cable.",band,support,params={"steps":steps},dimensions=["accuracy","reading","sequencing"])

def reading_exam(phase,seed,band,support,task_id):
    text="Nora usually cycles to school. Today her bike has a flat tyre, so her father is driving her. The text does not say how she will travel home."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.reading.exam-strategy",f"Read: {text} For the statement 'Nora will go home by car', decide true, false or not given and justify using textual evidence. Explain why guessing from the morning journey would be unsafe.",band,support,params={"text":text},dimensions=["reading","evidence_use","exam_strategy"],acceptable="not given; return journey is not stated")
    return task(task_id,"eng.y3.reading.exam-item",f"Read: {text} 'Nora will go home by car': true, false or not given?","not given",band,support,params={"text":text},dimensions=["accuracy","reading","exam_strategy"])

def listening_conversations(phase,seed,band,support,task_id):
    r=_r(seed); time=r.choice(["six","half past six","seven"]); script=f"A: Shall we meet at six? B: I can't. My lesson finishes at six. How about half past six? A: Perfect. Let's meet outside the cinema at {time if time!='six' else 'half past six'}."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.listening.conversation.turns","Listen to the tutor reading a short conversation. Note the first proposal, the problem, the counterproposal and the final agreement.",band,support,params={"tutor_script":script},dimensions=["listening","interaction_understanding","note_taking"],acceptable="captures proposal, reason, counterproposal and final agreement")
    return task(task_id,"eng.y3.listening.conversation.detail","Listen to the tutor reading the conversation. Why is the first meeting time rejected?","because the lesson finishes at six",band,support,params={"tutor_script":script},dimensions=["accuracy","listening","detail"],extra_solution={"tutor_script":script})

def listening_interview(phase,seed,band,support,task_id):
    r=_r(seed); job=r.choice(["paramedic","web designer","chef"]); script=f"Interviewer: What do you like about being a {job}? Speaker: I enjoy solving problems and working with people. The hours can be difficult, but I learn something new every week."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.listening.interview.paraphrase","Listen to the tutor reading the interview. State the job, one positive point and one difficulty using different words from the script where possible.",band,support,params={"tutor_script":script,"job":job},dimensions=["listening","paraphrase","gist_detail"],acceptable=f"job {job}; enjoyment of problem solving/people; difficult hours")
    return task(task_id,"eng.y3.listening.interview.gist","Listen to the tutor reading the interview. What difficulty does the speaker mention?","the hours can be difficult",band,support,params={"tutor_script":script},dimensions=["accuracy","listening","detail"],extra_solution={"tutor_script":script})

def listening_exam(phase,seed,band,support,task_id):
    script="The museum tour begins at eleven, but visitors should arrive fifteen minutes earlier. Tickets bought online can be collected at Desk B, not at the main entrance."
    if phase_mode(phase)=="transfer":
        return open_task(task_id,"eng.y3.listening.exam-strategy","Listen to the tutor reading the announcement twice. On the first listen note the situation; on the second listen note start time, arrival time and collection point. Explain why writing every word would be inefficient.",band,support,params={"tutor_script":script},dimensions=["listening","exam_strategy","note_taking"],acceptable="tour 11:00; arrive 10:45; Desk B; selective notes")
    return task(task_id,"eng.y3.listening.exam-item","Listen to the tutor reading the announcement. Where are online tickets collected?","Desk B",band,support,params={"tutor_script":script},dimensions=["accuracy","listening","detail"],extra_solution={"tutor_script":script})

ENGLISH_Y3_RECEPTIVE_BUILDERS={
    "eng.reading.a2_everyday_texts":reading_everyday,
    "eng.reading.a2_articles_biographies":reading_article,
    "eng.reading.a2_instructions":reading_instructions,
    "eng.reading.a2_exam_strategies":reading_exam,
    "eng.listening.a2_conversations":listening_conversations,
    "eng.listening.a2_announcements_interviews":listening_interview,
    "eng.listening.a2_exam_strategies":listening_exam,
}
