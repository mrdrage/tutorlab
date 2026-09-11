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
        {"text": "Durante l'intervallo la biblioteca della scuola resta aperta. Chi vuole prendere un libro deve registrare il prestito prima del rientro in classe.", "gist": "regole pratiche per il prestito in biblioteca", "facts": ["la biblioteca è aperta durante l'intervallo", "il prestito va registrato prima del rientro"]},
        {"text": "Marta arrivò alla fermata con qualche minuto di anticipo. Notò però che il tabellone indicava un ritardo e decise di avvisare sua sorella.", "gist": "Marta reagisce a un ritardo del mezzo", "facts": ["Marta arriva in anticipo", "avvisa sua sorella dopo aver letto il ritardo"]},
        {"text": "Ridurre gli sprechi d'acqua richiede piccoli comportamenti quotidiani: chiudere il rubinetto quando non serve e controllare eventuali perdite.", "gist": "azioni quotidiane per ridurre lo spreco d'acqua", "facts": ["chiudere il rubinetto quando non serve", "controllare eventuali perdite"]},
        {"text": "Nel quartiere è stato aperto un nuovo spazio per lo studio pomeridiano. L'accesso è gratuito, ma per i laboratori del venerdì occorre prenotarsi.", "gist": "nuovo spazio gratuito per lo studio con laboratori su prenotazione", "facts": ["l'accesso allo spazio è gratuito", "i laboratori del venerdì richiedono prenotazione"]},
        {"text": "Il consiglio degli studenti propone di aumentare le rastrelliere per le biciclette. Secondo i promotori, la misura renderebbe più semplice arrivare a scuola senza automobile.", "gist": "proposta per favorire l'uso della bicicletta a scuola", "facts": ["si propongono più rastrelliere", "l'obiettivo è facilitare gli spostamenti senza automobile"]},
    ],
    "french": [
        {"text": "Je m'appelle Léa. J'habite à Lyon avec ma famille. Le mercredi, je joue au basket avec mes amis.", "gist": "Léa se présente et parle de sa routine", "facts": ["elle habite à Lyon", "elle joue au basket le mercredi"]},
        {"text": "Samedi, le musée ouvre à dix heures. L'entrée coûte six euros et le café ferme à cinq heures.", "gist": "informations pratiques sur le musée", "facts": ["le musée ouvre à dix heures", "l'entrée coûte six euros"]},
        {"text": "Paul va à l'école en bus. Aujourd'hui le bus est en retard, alors il envoie un message à son ami.", "gist": "Paul prévient son ami à cause d'un retard", "facts": ["Paul va à l'école en bus", "il envoie un message à son ami"]},
        {"text": "Pour la sortie de classe, rendez-vous devant l'école à huit heures. Prenez un sandwich et une bouteille d'eau. Le retour est prévu à seize heures.", "gist": "consignes pratiques pour une sortie scolaire", "facts": ["le rendez-vous est à huit heures", "le retour est prévu à seize heures"]},
        {"text": "Camille cherche un cadeau pour sa sœur. Elle préfère un livre, mais elle veut dépenser moins de quinze euros.", "gist": "Camille cherche un cadeau avec un budget", "facts": ["elle préfère un livre", "elle veut dépenser moins de quinze euros"]},
    ],
    "spanish": [
        {"text": "Me llamo Clara y vivo en Valencia con mi familia. Los martes juego al voleibol con mis amigas.", "gist": "Clara se presenta y habla de su rutina", "facts": ["vive en Valencia", "juega al voleibol los martes"]},
        {"text": "El sábado el museo abre a las diez. La entrada cuesta seis euros y la cafetería cierra a las cinco.", "gist": "información práctica sobre el museo", "facts": ["el museo abre a las diez", "la entrada cuesta seis euros"]},
        {"text": "Pablo va al instituto en autobús. Hoy el autobús llega tarde, así que manda un mensaje a su amigo.", "gist": "Pablo avisa a su amigo por un retraso", "facts": ["Pablo va al instituto en autobús", "manda un mensaje a su amigo"]},
        {"text": "Para la excursión, quedamos delante del instituto a las ocho. Lleva un bocadillo y una botella de agua. Volvemos a las cuatro.", "gist": "instrucciones prácticas para una excursión", "facts": ["quedan a las ocho", "vuelven a las cuatro"]},
        {"text": "Lucía busca un regalo para su hermano. Prefiere un libro, pero quiere gastar menos de quince euros.", "gist": "Lucía busca un regalo con un presupuesto", "facts": ["prefiere un libro", "quiere gastar menos de quince euros"]},
    ],
}

LISTENING_BANK = {
    "italian": [
        {"script": "Domani il laboratorio inizierà alle nove e terminerà alle undici. Portate il quaderno, ma non serve il libro.", "gist": "orario e materiale del laboratorio", "facts": ["inizia alle nove", "serve il quaderno"]},
        {"script": "La visita è stata spostata a venerdì. Ci incontriamo davanti alla scuola alle otto e trenta e rientriamo nel primo pomeriggio.", "gist": "nuove informazioni sulla visita", "facts": ["la visita è venerdì", "l'incontro è alle otto e trenta"]},
        {"script": "La palestra oggi chiude alle diciotto. Il corso delle diciassette si svolge regolarmente, ma quello serale è annullato.", "gist": "cambiamenti nell'orario della palestra", "facts": ["la palestra chiude alle diciotto", "il corso serale è annullato"]},
        {"script": "Per il lavoro di gruppo portate una fonte stampata e una digitale. Avrete venti minuti per confrontarle prima della discussione.", "gist": "materiali e tempi per un lavoro di gruppo", "facts": ["servono due tipi di fonte", "ci sono venti minuti per confrontarle"]},
    ],
    "french": [
        {"script": "Bonjour. Le train pour Paris part à neuf heures vingt du quai quatre. Il a dix minutes de retard.", "gist": "annonce de train", "facts": ["départ à neuf heures vingt", "dix minutes de retard"]},
        {"script": "Salut Emma. On se retrouve samedi à trois heures devant le cinéma. Si tu es en retard, envoie-moi un message.", "gist": "rendez-vous au cinéma", "facts": ["samedi à trois heures", "devant le cinéma"]},
        {"script": "Le cours de sport commence à quatre heures. Apportez des chaussures propres et une bouteille d'eau.", "gist": "horaire et matériel pour le sport", "facts": ["le cours commence à quatre heures", "il faut des chaussures propres"]},
        {"script": "Pour aller au musée, prenez le bus douze et descendez à la troisième station. Le musée est en face du parc.", "gist": "itinéraire pour aller au musée", "facts": ["prendre le bus douze", "descendre à la troisième station"]},
    ],
    "spanish": [
        {"script": "Buenos días. El tren para Madrid sale a las nueve y veinte del andén cuatro. Lleva diez minutos de retraso.", "gist": "anuncio de tren", "facts": ["sale a las nueve y veinte", "lleva diez minutos de retraso"]},
        {"script": "Hola, Ana. Quedamos el sábado a las tres delante del cine. Si llegas tarde, mándame un mensaje.", "gist": "una cita en el cine", "facts": ["el sábado a las tres", "delante del cine"]},
        {"script": "La clase de deporte empieza a las cuatro. Trae unas zapatillas limpias y una botella de agua.", "gist": "horario y material para deporte", "facts": ["empieza a las cuatro", "hay que llevar zapatillas limpias"]},
        {"script": "Para ir al museo, toma el autobús doce y baja en la tercera parada. El museo está enfrente del parque.", "gist": "itinerario para ir al museo", "facts": ["tomar el autobús doce", "bajar en la tercera parada"]},
    ],
}

SCENARIOS = {
    "italian": ["una situazione scolastica", "un episodio della vita quotidiana", "un testo di studio", "un breve confronto tra due punti di vista", "una comunicazione digitale", "un'attività di gruppo"],
    "french": ["une journée d'école", "un week-end avec des amis", "une petite situation de voyage", "un échange dans un magasin", "un rendez-vous", "une activité en ville"],
    "spanish": ["un día de clase", "un fin de semana con amigos", "una situación sencilla de viaje", "una conversación en una tienda", "una cita", "una actividad en la ciudad"],
}

RESOURCE_SAMPLES = {
    "italian": {
        "grammar": ["Il ragazzo legge ogni sera.", "I miei amici sono arrivati presto.", "Quando piove, porto l'ombrello.", "Ho finito il compito che mi avevi indicato.", "Se avessi più tempo, leggerei di più.", "Marta, che vive vicino alla scuola, arriva a piedi."],
        "vocabulary": ["preciso, accurato, approssimativo", "causa, conseguenza, motivo", "sostenere, affermare, confutare", "inizio, sviluppo, conclusione", "registro formale, neutro, informale", "tema, informazione, inferenza"],
        "phonology": ["gli / figlio / foglia", "gn / bagno / sogno", "sc / scena / scegliere", "àncora / ancóra", "pèsca / pésca", "intonazione di domanda e affermazione"],
    },
    "french": {
        "grammar": ["Je suis italien et j'habite à Naples.", "Tu as un frère ? Oui, j'ai un frère.", "Nous allons à l'école à huit heures.", "Elle ne regarde pas la télévision le matin.", "Hier, j'ai visité le musée avec ma classe.", "Demain, je vais faire mes devoirs après le déjeuner."],
        "vocabulary": ["la famille : mère, père, frère, sœur", "l'école : classe, professeur, cahier, devoirs", "la ville : gare, musée, parc, magasin", "les loisirs : sport, musique, cinéma, lecture", "le temps : aujourd'hui, demain, hier, matin", "les achats : prix, taille, argent, cadeau"],
        "phonology": ["tu / tout", "bon / bonne", "rue / roue", "français / garçon", "petit ami (liaison possible en contexte)", "intonation d'une question courte"],
    },
    "spanish": {
        "grammar": ["Soy italiano y vivo en Nápoles.", "¿Tienes hermanos? Sí, tengo una hermana.", "Vamos al instituto a las ocho.", "Ella no ve la televisión por la mañana.", "Ayer visité el museo con mi clase.", "Mañana voy a hacer los deberes después de comer."],
        "vocabulary": ["la familia: madre, padre, hermano, hermana", "el instituto: clase, profesor, cuaderno, deberes", "la ciudad: estación, museo, parque, tienda", "el tiempo libre: deporte, música, cine, lectura", "el tiempo: hoy, mañana, ayer, por la mañana", "las compras: precio, talla, dinero, regalo"],
        "phonology": ["pero / perro", "caro / carro", "casa / queso", "gente / gato", "llave / calle", "entonación de una pregunta breve"],
    },
}

DIMENSIONS = {
    "grammar": ["accuracy", "independence", "stability"], "vocabulary": ["accuracy", "independence", "stability"], "phonology": ["accuracy", "fluency", "independence"],
    "reading": ["accuracy", "transfer", "stability"], "listening": ["accuracy", "transfer", "stability"], "interaction": ["independence", "transfer", "accuracy"],
    "spoken_production": ["independence", "transfer", "accuracy"], "writing": ["independence", "transfer", "accuracy"], "mediation": ["transfer", "independence", "explanation"],
    "intercultural": ["transfer", "explanation", "independence"], "learning_strategy": ["independence", "transfer", "explanation"], "oral": ["independence", "transfer", "explanation"],
    "text_analysis": ["accuracy", "explanation", "transfer"], "study_strategy": ["independence", "transfer", "explanation"], "integrated": ["independence", "transfer", "accuracy"],
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
    strand = node["strand"]
    sample = rng.choice(RESOURCE_SAMPLES[subject][strand])
    focus = rng.choice(["forma", "significato", "contrasto", "correzione"])

    if strand == "grammar":
        if mode == "model":
            prompt = f"{label}. Modello: {sample} Osserva come funziona «{node['title']}». Individua la parte decisiva e spiega, con una frase breve, perché il modello è corretto nel contesto."
        elif mode == "guided":
            prompt = f"{label}. Parti da questo modello: {sample} Trasformalo per adattarlo a {scenario}, modificando un solo elemento alla volta. Poi controlla «{node['title']}»."
        elif mode == "transfer":
            prompt = f"{label}. Usa «{node['title']}» in un contesto nuovo, {scenario}. Produci 2-3 enunciati autonomi e giustifica una scelta di forma o significato. Modello di riferimento, da non copiare: {sample}"
        else:
            prompt = f"{label}. Analizza il modello «{sample}», poi produci 2 esempi diversi che dimostrino questo obiettivo: {objective}."
    elif strand == "vocabulary":
        if mode == "model":
            prompt = f"{label}. Modello di uso lessicale: {sample}. Osserva come le parole appartengono allo stesso campo o svolgono funzioni diverse. Il tutor mostra un esempio d'uso; individua quale scelta lessicale rende il messaggio più preciso e spiega perché."
        elif mode == "guided":
            prompt = f"{label}. Usa almeno due elementi di questo lessico, {sample}, per completare un breve messaggio relativo a {scenario}."
        elif mode == "transfer":
            prompt = f"{label}. Senza tradurre parola per parola, usa il lessico collegato a «{node['title']}» per risolvere una situazione nuova: {scenario}. Parti da questo repertorio solo come appoggio: {sample}."
        else:
            prompt = f"{label}. Lessico di partenza: {sample}. Produci 2-3 enunciati autonomi che dimostrino: {objective}."
    else:
        if mode == "model":
            prompt = f"{label}. Modello fonologico: {sample}. Ascolta/leggi il modello del tutor, individua il contrasto rilevante e ripetilo mantenendo la distinzione."
        elif mode == "guided":
            prompt = f"{label}. Lavora sul campione «{sample}». Leggi o ripeti gli elementi, poi indica quale tratto sonoro o intonativo stai controllando."
        elif mode == "transfer":
            prompt = f"{label}. Applica il tratto osservato in «{sample}» a parole o frasi nuove collegate a {scenario}; il tutor valuta intelligibilità e controllo, non l'accento nativo."
        else:
            prompt = f"{label}. Usa il campione «{sample}» per dimostrare: {objective}. Il tutor valuta intelligibilità, discriminazione e controllo del tratto."

    return open_task(
        task_id, f"{node['id']}.language-resource", prompt, band, support,
        params={"scenario": scenario, "phase_mode": mode, "sample": sample, "focus": focus},
        dimensions=DIMENSIONS.get(strand, ["accuracy", "independence"]), rubric=_rubric(node),
        acceptable="Produzione o analisi corretta, comprensibile e coerente con il contesto.", errors=node.get("diagnostic_signals", []),
    )


def _reading_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    entry = rng.choice(READING_BANK[subject])
    text, gist, facts = entry["text"], entry["gist"], entry["facts"]
    mode = phase_mode(phase)
    focus = rng.choice(["gist", "detail", "evidence", "inference"])
    if mode == "model":
        prompt = f"Leggi il testo. Modello di comprensione: idea principale = «{gist}»; un dettaglio verificabile = «{facts[0]}». Individua nel testo le parole che sostengono il dettaglio e spiega perché il modello non aggiunge informazioni esterne.\n\n{text}"
    elif mode == "guided":
        prompt = f"Leggi il testo. L'idea principale riguarda «{gist}». Trova tu due dettagli che la sostengono e cita il punto del testo da cui li ricavi.\n\n{text}"
    elif mode == "transfer":
        prompt = f"Leggi il testo e ricava: tema, due informazioni sostenute dal testo e una conclusione che NON è possibile affermare con certezza.\n\n{text}"
    else:
        prompt = f"Leggi il testo. Indica l'idea principale e due informazioni utili. Spiega quale parola o frase del testo sostiene una delle tue risposte.\n\n{text}"
    return open_task(task_id, f"{node['id']}.reading", prompt, band, support,
        params={"text": text, "phase_mode": mode, "focus": focus}, dimensions=DIMENSIONS["reading"], rubric=_rubric(node),
        acceptable="Comprensione fondata su informazioni effettivamente presenti nel testo.", errors=node.get("diagnostic_signals", []))


def _listening_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    entry = rng.choice(LISTENING_BANK[subject])
    script, gist, facts = entry["script"], entry["gist"], entry["facts"]
    mode = phase_mode(phase)
    focus = rng.choice(["gist", "detail", "keywords", "sequence"])
    if mode == "model":
        prompt = f"Ascolta il messaggio letto dal tutor. Dopo il primo ascolto osserva questo modello di appunti: tema = «{gist}»; dettaglio utile = «{facts[0]}». Al secondo ascolto individua un'altra informazione e spiega perché è rilevante."
    elif mode == "guided":
        prompt = f"Ascolta il messaggio letto dal tutor. Il tema generale riguarda «{gist}». Annota due parole chiave e ricostruisci due informazioni pratiche senza chiedere la trascrizione completa."
    else:
        prompt = "Ascolta il breve messaggio letto dal tutor. Indica il tema e annota due informazioni pratiche senza chiedere la trascrizione completa."
    return task(task_id, f"{node['id']}.listening", prompt, "valutazione tramite rubrica", band, support,
        response_mode="open_response", params={"phase_mode": mode, "focus": focus}, dimensions=DIMENSIONS["listening"],
        errors=node.get("diagnostic_signals", []), rubric=_rubric(node), extra_solution={"tutor_script": script, "expected_gist": gist, "expected_facts": facts})


def _productive_task(subject, node, phase, seed, band, support, task_id):
    rng = random.Random(seed)
    scenario = rng.choice(SCENARIOS[subject])
    objective = rng.choice(node.get("objectives", [node["title"]]))
    mode = phase_mode(phase)
    audience = rng.choice(["un compagno", "il tutor", "un gruppo", "un destinatario esterno"])
    prompts = {
        "interaction": f"Simula uno scambio di almeno 4 turni in {scenario}. Obiettivo: {objective}. Inserisci una richiesta di chiarimento o una reazione reale alla risposta dell'altro.",
        "spoken_production": f"Prepara un breve intervento su {scenario}. Obiettivo: {objective}. Organizza apertura, 2-3 punti e chiusura.",
        "writing": f"Scrivi un testo breve per {audience}, legato a {scenario}. Obiettivo: {objective}. Controlla completezza, coesione e registro prima di consegnare.",
        "mediation": f"Immagina di dover aiutare {audience} in {scenario}. Seleziona e riformula soltanto le informazioni necessarie affinché possa agire correttamente.",
        "oral": f"Intervieni oralmente su {scenario}. Obiettivo: {objective}. Collega il tuo intervento a ciò che è già stato detto e motiva almeno una scelta.",
        "text_analysis": f"Analizza un breve testo relativo a {scenario} concentrandoti su «{node['title']}». Formula due osservazioni e sostienile con elementi del testo.",
        "study_strategy": f"Applica «{node['title']}» a {scenario}. Mostra il prodotto finale e descrivi in 2 passaggi la strategia usata.",
        "learning_strategy": f"Per {scenario}, scegli una strategia utile a «{node['title']}», applicala e spiega quando cambieresti strategia.",
        "intercultural": f"Confronta due esempi relativi a {scenario}. Descrivi una somiglianza e una differenza senza trasformare il singolo esempio in una regola generale.",
        "integrated": f"Compito integrato su {scenario}: ricava due informazioni, usale per prendere una decisione e comunica la decisione in modo adatto a {audience}.",
    }
    if mode == "model":
        structure = "apertura → informazione/idea principale → dettaglio o motivo → chiusura"
        prompt = f"Modello di struttura: {structure}. Osserva questa sequenza e applicala in forma molto breve a {scenario}. Obiettivo: {objective}."
    elif mode == "guided":
        prompt = f"Usa questa scaletta: apertura → 2 punti → chiusura. Completa il compito su {scenario}. Obiettivo: {objective}."
    else:
        prompt = prompts.get(node["strand"], f"Svolgi un compito su {scenario} che dimostri: {objective}.")
    return open_task(task_id, f"{node['id']}.productive", prompt, band, support,
        params={"scenario": scenario, "phase_mode": mode, "audience": audience, "objective": objective},
        dimensions=DIMENSIONS.get(node["strand"], ["independence", "transfer"]), rubric=_rubric(node),
        acceptable="Risposta pertinente, completa e coerente con lo scopo comunicativo.", errors=node.get("diagnostic_signals", []))


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
