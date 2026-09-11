from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Callable

from engine.generation_common import open_task, phase_mode, task

ROOT = Path(__file__).resolve().parents[1]

SUBJECT_CONFIG = {
    "italian": {"prefix": "ita", "label": "Italiano"},
    "french": {"prefix": "fr", "label": "Francese"},
    "spanish": {"prefix": "es", "label": "Spagnolo"},
}

READING_BANK = {
    "italian": [
        "Durante l'intervallo la biblioteca della scuola resta aperta. Chi vuole prendere un libro deve registrare il prestito prima del rientro in classe.",
        "Marta arrivò alla fermata con qualche minuto di anticipo. Notò però che il tabellone indicava un ritardo e decise di avvisare sua sorella.",
        "Ridurre gli sprechi d'acqua richiede piccoli comportamenti quotidiani: chiudere il rubinetto quando non serve e controllare eventuali perdite.",
    ],
    "french": [
        "Je m'appelle Léa. J'habite à Lyon avec ma famille. Le mercredi, je joue au basket avec mes amis.",
        "Samedi, le musée ouvre à dix heures. L'entrée coûte six euros et le café ferme à cinq heures.",
        "Paul va à l'école en bus. Aujourd'hui le bus est en retard, alors il envoie un message à son ami.",
    ],
    "spanish": [
        "Me llamo Clara y vivo en Valencia con mi familia. Los martes juego al voleibol con mis amigas.",
        "El sábado el museo abre a las diez. La entrada cuesta seis euros y la cafetería cierra a las cinco.",
        "Pablo va al instituto en autobús. Hoy el autobús llega tarde, así que manda un mensaje a su amigo.",
    ],
}

LISTENING_BANK = {
    "italian": [
        "Domani il laboratorio inizierà alle nove e terminerà alle undici. Portate il quaderno, ma non serve il libro.",
        "La visita è stata spostata a venerdì. Ci incontriamo davanti alla scuola alle otto e trenta e rientriamo nel primo pomeriggio.",
    ],
    "french": [
        "Bonjour. Le train pour Paris part à neuf heures vingt du quai quatre. Il a dix minutes de retard.",
        "Salut Emma. On se retrouve samedi à trois heures devant le cinéma. Si tu es en retard, envoie-moi un message.",
    ],
    "spanish": [
        "Buenos días. El tren para Madrid sale a las nueve y veinte del andén cuatro. Lleva diez minutos de retraso.",
        "Hola, Ana. Quedamos el sábado a las tres delante del cine. Si llegas tarde, mándame un mensaje.",
    ],
}

SCENARIOS = {
    "italian": [
        "una situazione scolastica",
        "un episodio della vita quotidiana",
        "un testo di studio",
        "un breve confronto tra due punti di vista",
    ],
    "french": [
        "une journée d'école",
        "un week-end avec des amis",
        "une petite situation de voyage",
        "un échange dans un magasin",
    ],
    "spanish": [
        "un día de clase",
        "un fin de semana con amigos",
        "una situación sencilla de viaje",
        "una conversación en una tienda",
    ],
}

DIMENSIONS = {
    "grammar": ["accuracy", "independence", "stability"],
    "vocabulary": ["accuracy", "independence", "stability"],
    "phonology": ["accuracy", "fluency", "independence"],
    "reading": ["accuracy", "transfer", "stability"],
    "listening": ["accuracy", "transfer", "stability"],
    "interaction": ["independence", "transfer", "accuracy"],
    "spoken_production": ["independence", "transfer", "accuracy"],
    "writing": ["independence", "transfer", "accuracy"],
    "mediation": ["transfer", "independence", "explanation"],
    "intercultural": ["transfer", "explanation", "independence"],
    "learning_strategy": ["independence", "transfer", "explanation"],
    "oral": ["independence", "transfer", "explanation"],
    "text_analysis": ["accuracy", "explanation", "transfer"],
    "study_strategy": ["independence", "transfer", "explanation"],
    "integrated": ["independence", "transfer", "accuracy"],
}


def _load_node(subject: str, competency_id: str) -> dict[str, Any]:
    base = ROOT / "curriculum" / "middle-school" / subject
    for year in (1, 2, 3):
        data = json.loads((base / f"year-{year}.json").read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            if node.get("id") == competency_id:
                return node
    raise ValueError(f"competency not found: {competency_id}")


def _subject_from_id(competency_id: str) -> str:
    prefix = competency_id.split(".", 1)[0]
    for subject, config in SUBJECT_CONFIG.items():
        if config["prefix"] == prefix:
            return subject
    raise ValueError(f"unsupported language competency: {competency_id}")


def _rubric(node: dict[str, Any]) -> dict[str, str]:
    evidence = node.get("mastery_evidence", [])
    text = " ".join(evidence[:2]) if evidence else "La risposta dimostra la competenza richiesta in modo pertinente e comprensibile."
    return {"full_credit": text}


def _language_resource_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    label = SUBJECT_CONFIG[subject]["label"]
    objective = rng.choice(node.get("objectives", [node["title"]]))
    scenario = rng.choice(SCENARIOS[subject])
    mode = phase_mode(phase)
    if mode == "model":
        prompt = f"{label}. Osserva la competenza «{node['title']}» nel contesto di {scenario}. Produci un esempio corretto e spiega in una frase quale regola o scelta rende l'esempio appropriato."
    elif mode == "guided":
        prompt = f"{label}. Completa un mini-esempio su {scenario} applicando «{node['title']}». Poi modifica un elemento della frase senza perdere correttezza."
    elif mode == "transfer":
        prompt = f"{label}. Usa «{node['title']}» in un contesto nuovo: {scenario}. Crea 2-3 enunciati e giustifica una scelta linguistica."
    else:
        prompt = f"{label}. Dimostra questa competenza: {objective}. Lavora su {scenario} con 2-3 esempi autonomi."
    return open_task(
        task_id,
        f"{node['id']}.language-resource",
        prompt,
        band,
        support,
        params={"scenario": scenario, "phase_mode": mode},
        dimensions=DIMENSIONS.get(node["strand"], ["accuracy", "independence"]),
        rubric=_rubric(node),
        acceptable="Produzione corretta, comprensibile e coerente con il contesto.",
        errors=node.get("diagnostic_signals", []),
    )


def _reading_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    text = rng.choice(READING_BANK[subject])
    mode = phase_mode(phase)
    if mode == "transfer":
        prompt = f"Leggi il testo e ricava: tema, due informazioni sostenute dal testo e una conclusione che NON è possibile affermare con certezza.\n\n{text}"
    else:
        prompt = f"Leggi il testo. Indica l'idea principale e due informazioni utili. Spiega quale parola o frase del testo sostiene una delle tue risposte.\n\n{text}"
    return open_task(
        task_id,
        f"{node['id']}.reading",
        prompt,
        band,
        support,
        params={"text": text, "phase_mode": mode},
        dimensions=DIMENSIONS["reading"],
        rubric=_rubric(node),
        acceptable="Comprensione fondata su informazioni effettivamente presenti nel testo.",
        errors=node.get("diagnostic_signals", []),
    )


def _listening_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    script = rng.choice(LISTENING_BANK[subject])
    prompt = "Ascolta il breve messaggio letto dal tutor. Indica il tema e annota due informazioni pratiche senza chiedere la trascrizione completa."
    return task(
        task_id,
        f"{node['id']}.listening",
        prompt,
        "valutazione tramite rubrica",
        band,
        support,
        response_mode="open_response",
        params={"phase_mode": phase_mode(phase)},
        dimensions=DIMENSIONS["listening"],
        errors=node.get("diagnostic_signals", []),
        rubric=_rubric(node),
        extra_solution={"tutor_script": script},
    )


def _productive_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    scenario = rng.choice(SCENARIOS[subject])
    objective = rng.choice(node.get("objectives", [node["title"]]))
    prompts = {
        "interaction": f"Simula uno scambio di almeno 4 turni in {scenario}. Obiettivo: {objective}. Inserisci una richiesta di chiarimento o una reazione reale alla risposta dell'altro.",
        "spoken_production": f"Prepara un breve intervento su {scenario}. Obiettivo: {objective}. Organizza apertura, 2-3 punti e chiusura.",
        "writing": f"Scrivi un testo breve legato a {scenario}. Obiettivo: {objective}. Controlla completezza, coesione e registro prima di consegnare.",
        "mediation": f"Immagina di dover aiutare un compagno in {scenario}. Seleziona e riformula soltanto le informazioni necessarie affinché possa agire correttamente.",
        "oral": f"Intervieni oralmente su {scenario}. Obiettivo: {objective}. Collega il tuo intervento a ciò che è già stato detto e motiva almeno una scelta.",
        "text_analysis": f"Analizza un breve testo relativo a {scenario} concentrandoti su «{node['title']}». Formula due osservazioni e sostienile con elementi del testo.",
        "study_strategy": f"Applica «{node['title']}» a {scenario}. Mostra il prodotto finale e descrivi in 2 passaggi la strategia usata.",
        "learning_strategy": f"Per {scenario}, scegli una strategia utile a «{node['title']}», applicala e spiega quando cambieresti strategia.",
        "intercultural": f"Confronta due esempi relativi a {scenario}. Descrivi una somiglianza e una differenza senza trasformare il singolo esempio in una regola generale.",
        "integrated": f"Compito integrato su {scenario}: ricava due informazioni, usale per prendere una decisione e comunica la decisione in modo adatto al destinatario.",
    }
    prompt = prompts.get(node["strand"], f"Svolgi un compito su {scenario} che dimostri: {objective}.")
    return open_task(
        task_id,
        f"{node['id']}.productive",
        prompt,
        band,
        support,
        params={"scenario": scenario, "phase_mode": phase_mode(phase)},
        dimensions=DIMENSIONS.get(node["strand"], ["independence", "transfer"]),
        rubric=_rubric(node),
        acceptable="Risposta pertinente, completa e coerente con lo scopo comunicativo.",
        errors=node.get("diagnostic_signals", []),
    )


def build_language_task(competency_id: str, phase: str, seed: int, band: int, support: str, task_id: str):
    subject = _subject_from_id(competency_id)
    node = _load_node(subject, competency_id)
    strand = node["strand"]
    if strand in {"grammar", "vocabulary", "phonology"}:
        return _language_resource_task(subject, node, phase, seed, band, support, task_id)
    if strand == "reading":
        return _reading_task(subject, node, phase, seed, band, support, task_id)
    if strand == "listening":
        return _listening_task(subject, node, phase, seed, band, support, task_id)
    return _productive_task(subject, node, phase, seed, band, support, task_id)


def _builder(competency_id: str) -> Callable:
    def build(phase, seed, band, support, task_id):
        return build_language_task(competency_id, phase, seed, band, support, task_id)
    return build


def registry_for_subject(subject: str) -> dict[str, Callable]:
    if subject not in SUBJECT_CONFIG:
        raise ValueError(f"unsupported language subject: {subject}")
    base = ROOT / "curriculum" / "middle-school" / subject
    registry = {}
    for year in (1, 2, 3):
        path = base / f"year-{year}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            registry[node["id"]] = _builder(node["id"])
    return registry
