from engine.session_engine import student_view

TEACHING_PHASES={"essential_explanation","worked_example","targeted_model","guided_practice","faded_practice"}


def validate_session(session,policy):
    errors=[]
    action=session.get("action")
    kinds=[p.get("kind") for p in session.get("phases",[])]
    expected=policy.get("phase_templates",{}).get(action)
    if expected and kinds!=expected: errors.append("phase template mismatch")

    task_ids=[]; fingerprints=[]
    for phase in session.get("phases",[]):
        for task in phase.get("tasks",[]):
            task_ids.append(task.get("task_id")); fingerprints.append(task.get("fingerprint"))
            if task.get("challenge_band") not in {1,2,3,4,5}: errors.append("invalid challenge band")
            if task.get("competency_id")!=session.get("target_competency_id"): errors.append("task competency mismatch")
    if len(task_ids)!=len(set(task_ids)): errors.append("duplicate task id")
    clean=[fp for fp in fingerprints if fp]
    if len(clean)!=len(set(clean)): errors.append("duplicate fingerprint in session")

    if action=="reassess":
        if any(kind in TEACHING_PHASES for kind in kinds): errors.append("reassess contains teaching phase")
        for phase in session.get("phases",[]):
            for task in phase.get("tasks",[]):
                if task.get("support_level")!="none": errors.append("reassess task uses scaffold")
    if action=="recover" and (not kinds or kinds[-1]!="reassessment"): errors.append("recover does not end with reassessment")
    if action=="advance" and "independent_practice" not in kinds: errors.append("advance lacks independent practice")
    if action in {"recover","advance","consolidate","extend"} and "transfer" not in kinds: errors.append("instructional session lacks transfer")

    sv=student_view(session)
    for phase in sv.get("phases",[]):
        for task in phase.get("tasks",[]):
            if any(key in task for key in ("solution","rubric","error_signals","generation_parameters")): errors.append("student view leaks tutor data")
    return errors
