import random

CASES=[("I","play","play"),("They","study","study"),("Marta","play","plays"),("Leo","study","studies"),("Anna","go","goes")]


def task(i,f,p,s,b,sup,mode="short_answer",params=None,dims=None,errors=None):
    return {"task_id":i,"family_id":f,"prompt":p,"response_mode":mode,"challenge_band":b,"support_level":sup,"solution":s,"rubric":{"full_credit":"Forma corretta e funzione coerente."},"evidence_dimensions":dims or ["accuracy"],"error_signals":errors or [],"generation_parameters":params or {}}


def present_simple_task(phase,seed,band,support,task_id):
    r=random.Random(seed); subject,base,form=r.choice(CASES); activity=r.choice(["tennis after school","English every day","TV in the evening","to school by bus"])
    params={"subject":subject,"base":base,"form":form,"activity":activity}
    if phase in {"diagnostic_check","retrieval","activation","contrast_task"}:
        wrong=base if form!=base else base+"s"
        p=f"Choose: A) {subject} {form} {activity}. B) {subject} {wrong} {activity}."
        return task(task_id,"eng.present-simple.form-choice",p,{"answer":"A"},band,support,"single_choice",params,["accuracy","form_control"],[{"pattern":"third_person_s","code":"procedure_error"}])
    if phase in {"worked_example","targeted_model"}:
        p="Study: 'She plays tennis.' Question: use does and return the main verb to base form -> 'Does she play tennis?'"
        return task(task_id,"eng.present-simple.worked-question",p,{"answer":"Does she play tennis?"},band,"worked_support","structured_steps",{},["explanation","form_control"])
    if phase in {"guided_practice","faded_practice"}:
        aux="Does" if form!=base else "Do"
        p=f"Turn into a question: '{subject} {form} {activity}.' Start with Do/Does."
        return task(task_id,"eng.present-simple.question-fade",p,{"answer":f"{aux} {subject.lower()} {base} {activity}?"},band,support,"structured_steps",params,["accuracy","independence","form_control"],[{"pattern":"s_after_does","code":"procedure_error"}])
    if phase in {"independent_practice","verification","reassessment"}:
        aux="doesn't" if form!=base else "don't"
        p=f"Write the negative form: '{subject} {form} {activity}.'"
        return task(task_id,"eng.present-simple.negative",p,{"answer":f"{subject} {aux} {base} {activity}."},band,support,"short_answer",params,["accuracy","independence","form_control"])
    if phase in {"transfer","transfer_probe","challenge"}:
        p="Write four true sentences about a weekly routine: affirmative, negative, third person, and one with a frequency word."
        return task(task_id,"eng.present-simple.routine-production",p,{"requirements":["affirmative","negative","third_person","frequency"]},band,support,"open_response",{"topic":"weekly_routine"},["transfer","independence","communicative_use"],[{"pattern":"rule_known_not_used","code":"not_automated"}])
    p="Correct and explain: 'She doesn't plays football on Monday.'"
    return task(task_id,"eng.present-simple.error-analysis",p,{"answer":"She doesn't play football on Monday.","key_idea":"after does/doesn't use the base form"},band,support,"open_response",{},["explanation","transfer","form_control"])
