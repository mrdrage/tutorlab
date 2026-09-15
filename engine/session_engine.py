from __future__ import annotations

import copy
import json
from pathlib import Path

from engine.curriculum_access import load_competency, subject_for_competency
from engine.task_families import build_unique_task

ROOT=Path(__file__).resolve().parents[1]
POLICY_PATH=ROOT/"config"/"session-policy.json"

TASK_PHASES={"diagnostic_check","retrieval","activation","contrast_task","worked_example","targeted_model","guided_practice","faded_practice","independent_practice","transfer","transfer_probe","verification","reassessment","challenge","strategy_comparison","explanation","reflection"}
EXTRA_TASK_PRIORITY=("independent_practice","guided_practice","faded_practice","verification","reassessment","transfer","transfer_probe","challenge","contrast_task","retrieval","activation","strategy_comparison")


def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _support(phase,action):
    if action=="reassess": return "none"
    if phase in {"worked_example","targeted_model"}: return "worked_support"
    if phase in {"guided_practice","faded_practice"}: return "structured_prompt"
    if phase in {"diagnostic_check","retrieval","activation","contrast_task"}: return "light_prompt" if action!="reassess" else "none"
    return "none"


def _band(base,phase):
    if phase in {"diagnostic_check","retrieval","activation"}: return max(1,base-1)
    if phase in {"transfer","transfer_probe","challenge","strategy_comparison","explanation"}: return min(5,base+1)
    return base


def _purpose(phase,competency):
    title=competency.get("title",competency.get("id","competenza"))
    texts={
        "diagnostic_check":f"Verificare il punto di partenza su {title}.",
        "retrieval":f"Richiamare conoscenze utili per {title}.",
        "activation":f"Attivare i prerequisiti necessari a {title}.",
        "essential_explanation":f"Presentare solo le idee indispensabili per {title}.",
        "worked_example":"Mostrare un modello completo con ragionamento esplicito.",
        "targeted_model":"Rimodellare il punto che ha prodotto errore.",
        "faded_practice":"Rimuovere gradualmente parti del supporto.",
        "guided_practice":"Far completare passaggi significativi con supporto temporaneo.",
        "independent_practice":"Raccogliere evidenza di autonomia.",
        "transfer":"Applicare la competenza in una forma meno familiare.",
        "transfer_probe":"Verificare se la competenza regge fuori dal formato abituale.",
        "verification":"Verificare padronanza sul target corrente.",
        "reassessment":"Controllare l'effetto del recupero prima di risalire all'obiettivo sospeso.",
        "contrast_task":"Discriminare tra due regole o strategie plausibili.",
        "challenge":"Aumentare scelta strategica e apertura del compito.",
        "strategy_comparison":"Confrontare strategie e criteri di scelta.",
        "explanation":"Rendere esplicito il ragionamento dello studente.",
        "reflection":"Far valutare strategia, supporto usato e prossimo miglioramento."
    }
    return texts.get(phase,phase.replace("_"," "))


def _instruction(phase,competency):
    if phase not in {"essential_explanation"}: return None
    objectives=competency.get("objectives",[])
    return {"title":competency.get("title"),"key_points":objectives[:3],"rule":"La spiegazione deve restare essenziale e collegata subito a un esempio."}


def _extra_task_phase_indexes(phases):
    ranked=[]
    for kind in EXTRA_TASK_PRIORITY:
        ranked.extend(index for index,phase in enumerate(phases) if phase.get("kind")==kind)
    return ranked


def build_session(target_competency_id,action,*,original_target_id=None,challenge_band=None,duration_minutes=None,quantity_hint=None,seed=1,history_fingerprints=None,policy=None):
    policy=policy or load_policy(); history=list(history_fingerprints or [])
    competency=load_competency(target_competency_id)
    subject=subject_for_competency(target_competency_id)
    if action not in policy["phase_templates"]: raise ValueError("unsupported action")
    base_band=challenge_band or policy["default_challenge_band_by_action"][action]
    duration=duration_minutes or policy["default_duration_minutes"]
    phases=[]; used=list(history); template=policy["phase_templates"][action]
    per=max(2,duration//max(1,len(template)))
    task_counter=0
    for index,kind in enumerate(template,1):
        phase={"phase_id":f"p{index}","kind":kind,"purpose":_purpose(kind,competency),"estimated_minutes":per,"tasks":[]}
        instruction=_instruction(kind,competency)
        if instruction: phase["instruction"]=instruction
        if kind in TASK_PHASES:
            task_counter+=1
            item=build_unique_task(target_competency_id,kind,seed+index*101,_band(base_band,kind),_support(kind,action),f"t{task_counter}",used,policy["max_generation_attempts"])
            phase["tasks"].append(item); used.append(item["fingerprint"])
        phases.append(phase)

    structural_minimum=task_counter
    requested=max(1,int(quantity_hint)) if quantity_hint is not None else structural_minimum
    extra_indexes=_extra_task_phase_indexes(phases)
    extra_cursor=0
    misses=0
    max_misses=max(1,len(extra_indexes)*3)
    while task_counter < requested and extra_indexes and misses < max_misses:
        phase_index=extra_indexes[extra_cursor % len(extra_indexes)]
        phase=phases[phase_index]
        kind=phase["kind"]
        next_task_number=task_counter+1
        item=build_unique_task(
            target_competency_id,
            kind,
            seed+5000+next_task_number*97+phase_index,
            _band(base_band,kind),
            _support(kind,action),
            f"t{next_task_number}",
            used,
            policy["max_generation_attempts"],
        )
        extra_cursor+=1
        if item["fingerprint"] in used:
            misses+=1
            continue
        task_counter=next_task_number
        misses=0
        phase["tasks"].append(item); used.append(item["fingerprint"])

    return {
        "version":"0.1","session_id":f"session-{target_competency_id.replace('.','-')}-{seed}","subject":subject,
        "target_competency_id":target_competency_id,"original_target_id":original_target_id or target_competency_id,
        "action":action,"challenge_band":base_band,"duration_minutes":duration,"seed":seed,
        "generation":{
            "engine_version":"0.1","history_fingerprints":history,"original_content":True,
            "task_quantity_requested":requested,"task_quantity_structural_minimum":structural_minimum,"task_quantity_actual":task_counter,
            "task_quantity_satisfied":task_counter>=requested,"task_quantity_shortfall":max(0,requested-task_counter),
        },"phases":phases
    }


def student_view(session):
    view=copy.deepcopy(session)
    view["generation"].pop("history_fingerprints",None)
    for phase in view["phases"]:
        for item in phase.get("tasks",[]):
            for key in ("solution","rubric","error_signals","generation_parameters"):
                item.pop(key,None)
    return view
