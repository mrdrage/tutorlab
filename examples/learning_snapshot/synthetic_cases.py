def state(competency_id,status,confidence,accuracy,independence,stability,transfer):
    return {
        "competency_id":competency_id,
        "status":status,
        "confidence":confidence,
        "mastery":{"accuracy":accuracy,"independence":independence,"stability":stability,"transfer":transfer},
        "evidence_summary":{"independent_event_count":4,"contradiction_level":0.0},
        "error_hypotheses":[],
    }


def mathematics_case():
    return {
        "version":"0.1",
        "subjects":{"mathematics":{"typical_year":1,"competency_states":{
            "math.numbers.fraction-meaning":state("math.numbers.fraction-meaning","secure",0.82,0.88,0.80,0.78,0.70),
            "math.numbers.divisibility":state("math.numbers.divisibility","secure",0.80,0.86,0.80,0.75,0.62),
            "math.numbers.fraction-equivalence":state("math.numbers.fraction-equivalence","developing",0.78,0.70,0.64,0.60,0.38),
        },"evidence_events":[],"objective_stack":None,"last_recommendation":None}},
        "recent_activity":{"session_ids":[],"fingerprints":[]},
        "preferences":{"default_duration_minutes":40,"max_challenge_band":4},
    }


def english_case():
    return {
        "version":"0.1",
        "subjects":{"english":{"typical_year":1,"competency_states":{
            "eng.grammar.be":state("eng.grammar.be","secure",0.84,0.90,0.82,0.80,0.66),
            "eng.grammar.present_simple":state("eng.grammar.present_simple","developing",0.76,0.72,0.62,0.58,0.42),
        },"evidence_events":[],"objective_stack":None,"last_recommendation":None}},
        "recent_activity":{"session_ids":[],"fingerprints":[]},
        "preferences":{"default_duration_minutes":35,"max_challenge_band":4},
    }
