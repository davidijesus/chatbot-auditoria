from typing import List, Dict
from src.ingest.email_parser import parse_emails
from src.utils.llm import chat

CONSPIRACY_TERMS = [
    "operação fênix",
    "apague este e-mail",
    "inimigo",
    "agente infiltrado",
    "toby",
    "destruir as evidências",
    "recibos",
    "mascarar",
    "deletar",
    "comprometida",
]

def _score_email(text: str) -> int:
    t = text.lower()
    return sum(1 for term in CONSPIRACY_TERMS if term in t)

def detect_conspiracy() -> Dict:
    emails = parse_emails()

    # pega candidatos fortes: menção a Toby + linguagem de conspiração
    candidates = []
    for e in emails:
        blob = f"{e.assunto}\n{e.mensagem}"
        score = _score_email(blob)
        if score >= 2 and ("toby" in blob.lower() or "flenderson" in blob.lower()):
            candidates.append((score, e))

    candidates.sort(key=lambda x: x[0], reverse=True)
    top = [e for _, e in candidates[:6]]

    evidences = []
    for e in top:
        snippet = e.mensagem.strip().replace("\n", " ")
        if len(snippet) > 240:
            snippet = snippet[:240] + "..."
        evidences.append({
            "email_id": f"email_{e.idx}",
            "de": e.de,
            "para": e.para,
            "data": e.data,
            "assunto": e.assunto,
            "trecho": snippet
        })

    # se não achou nada, já retorna inconclusivo com transparência
    if not evidences:
        return {
            "veredito": "inconclusivo",
            "resumo": "Não encontrei emails com sinais claros de conspiração contra o Toby usando os critérios atuais.",
            "evidencias": []
        }

    # LLM só para justificar com base nas evidências coletadas
    context = "\n\n".join(
        [f"[email_{ev['email_id'].split('_')[-1]}] De: {ev['de']} | Assunto: {ev['assunto']}\n{ev['trecho']}"
         for ev in evidences]
    )

    system = (
        "Você é um auditor. Dado apenas o conjunto de evidências (trechos de emails), "
        "decida se há indícios de conspiração do Michael Scott contra o Toby. "
        "Responda com: Veredito (há evidência / não há evidência / inconclusivo) e um resumo curto. "
        "Não invente nada fora do contexto."
    )
    user = (
        "Evidências:\n"
        f"{context}\n\n"
        "Responda em português e no final liste quais email_ids foram usados."
    )

    answer = chat(system, user)

    return {
        "veredito_e_resumo": answer,
        "evidencias": evidences
    }
