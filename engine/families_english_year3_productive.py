from __future__ import annotations

from engine.generation_common import open_task, phase_mode


def _skill_builder(comp_id,family,label,prompt,dimensions,acceptable):
    def build(phase,seed,band,support,task_id):
        mode=phase_mode(phase)
        lead={
            "model":"Follow the structure in the prompt and make each communicative move explicit. ",
            "guided":"Use the cues, but complete the content yourself. ",
            "check":"Respond briefly without a model. ",
            "independent":"Respond independently. ",
            "transfer":"Adapt the language to the situation instead of repeating a memorised formula. ",
        }[mode]
        return open_task(task_id,f"eng.y3.{family}.{mode}",lead+prompt,band,support,params={"skill":comp_id,"mode":mode,"seed":seed},dimensions=dimensions,acceptable=acceptable,rubric={"full_credit":f"{label}: message is understandable, relevant and sufficiently connected; required communicative functions are completed without tutor-side invention of a score."})
    return build


CONFIG={
"eng.interaction.opinions_agreement":("interaction.opinion","Opinion interaction","A partner says that school uniforms are useful. Give your view, agree or disagree with one point, and add a reason using because.",["interaction","meaning","cohesion"],"expresses a view, reacts to partner content and gives a reason"),
"eng.interaction.problem_solving_planning":("interaction.planning","Collaborative planning","You and a partner have €20 and two hours for an afternoon activity. Propose an option, react to a different option, use one if-clause for a consequence, and reach a final choice.",["interaction","problem_solving","negotiation"],"proposal + response + constraint handling + explicit decision"),
"eng.interaction.services_travel":("interaction.services","Service interaction","At a station your train is delayed and you do not know one useful word. Explain the problem, ask for the information you need, paraphrase the missing word and check one practical detail.",["interaction","paraphrase","detail"],"completes service exchange despite a lexical gap and verifies a detail"),
"eng.interaction.online_basic":("interaction.online","Online interaction","Write two short messages in an online group planning a class activity: respond to another person's idea, add one useful detail and ask one follow-up question.",["interaction","writing","pragmatics"],"messages are relevant to the thread and move the exchange forward"),
"eng.production.experience_future_opinion":("production.experience","Connected spoken production","Prepare a short spoken response that mentions one past experience, one future plan and one opinion with a reason. Connect the ideas clearly.",["spoken_production","cohesion","grammar_control"],"several connected sentences with coherent time reference and a reason"),
"eng.production.short_presentation":("production.presentation","Short presentation","Give a short presentation on a familiar topic with an opening, two organised points and a closing. Use notes as prompts rather than writing a full script, then prepare for one simple question.",["spoken_production","organisation","interaction_readiness"],"clear opening-development-closing and content that can support a follow-up question"),
"eng.writing.a2_email":("writing.email","A2 email","Write an email to a friend: invite them to an activity, explain when and where it happens, give one reason to come and ask for a reply. Include greeting and closing.",["writing","cohesion","task_completion"],"all content points covered with coherent informal register"),
"eng.writing.a2_narrative":("writing.narrative","A2 narrative","Write a short narrative about a day when a plan changed. Include setting, at least three events in order, a reaction and a final outcome. Use simple connectors.",["writing","sequencing","grammar_control"],"story is followable from setting through outcome with stable past reference"),
"eng.writing.opinion_text":("writing.opinion","A2 opinion text","Write a short opinion paragraph about whether phones should be used during school breaks. State a position, give two simple reasons and finish with a concluding sentence.",["writing","argumentation","cohesion"],"clear position, relevant reasons and connected conclusion"),
"eng.mediation.relay_specific_information":("mediation.relay","Relay information","A visitor needs only the opening time, ticket price and meeting point from a longer notice. Relay exactly those three details in simple English and leave out unrelated information.",["mediation","selection","accuracy"],"selects and relays requested details without distortion"),
"eng.mediation.explain_simple_text_data":("mediation.data","Explain simple data","A small table shows: bus 12 students, bike 8, walk 5. Explain the main pattern to a classmate in simple English, including the most and least common choices without inventing causes.",["mediation","data_interpretation","accuracy"],"preserves values/relations and makes the pattern accessible without unsupported inference"),
"eng.mediation.collaborative_meaning":("mediation.collaboration","Collaborative mediation","During a group task one person does not understand the current proposal. Restate it more simply, connect it to another person's idea and ask a question that checks understanding.",["mediation","interaction","clarification"],"simplifies, connects ideas and checks shared understanding"),
"eng.intercultural.pragmatics_compare":("intercultural.pragmatics","Intercultural pragmatics","Compare two possible ways of making a request in different situations. Explain which sounds more appropriate to a friend and which to an unfamiliar adult, without claiming that one culture always behaves in one fixed way.",["intercultural","pragmatics","reasoning"],"context-sensitive comparison using non-absolute language"),
"eng.learning.self_assessment_can_do":("learning.self-assessment","Can-do self assessment","Choose one recent English task and state what you can do now, what evidence from the task supports that judgment, and one specific next improvement. Keep reading, writing, listening or interaction distinct.",["metacognition","evidence_use","planning"],"judgment is tied to concrete evidence and a specific next priority"),
"eng.learning.paraphrase_compensation":("learning.paraphrase","Paraphrase strategy","Imagine you forget the English word for 'umbrella'. Keep speaking in English by describing its category, use and one visible feature until a listener could guess it.",["strategy_use","paraphrase","interaction"],"meaning is recoverable through description without switching language"),
}

ENGLISH_Y3_PRODUCTIVE_BUILDERS={
    cid:_skill_builder(cid,*spec) for cid,spec in CONFIG.items()
}
