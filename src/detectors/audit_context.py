import pandas as pd
from typing import Dict, List
from src.ingest.load_transactions import load_transactions_df
from src.ingest.email_parser import parse_emails
from src.utils.llm import chat
from src.rag.policy_rag import query_policy

FRAUD_EMAIL_TERMS = [
    "mascarar", "passar como", "nome genérico", "não escrevam", "apague este e-mail",
    "fraude", "não conta pra ninguém", "destruir as evidências", "recibos"
]

def audit_context() -> Dict:
    df = load_transactions_df()
    emails = parse_emails()

    cols = {c.lower(): c for c in df.columns}
    amount_col = cols.get("valor") or cols.get("amount") or cols.get("value")
    desc_col = cols.get("descricao") or cols.get("descrição") or cols.get("description") or cols.get("descricao_da_transacao")
    who_col = cols.get("funcionario") or cols.get("employee") or cols.get("user")

    if not amount_col or not desc_col:
        return {"erro": "CSV não tem colunas mínimas esperadas (valor e descrição).", "colunas": list(df.columns)}

    df["_desc_norm"] = df[desc_col].astype(str).str.lower()
    df["_amount_num"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

    # 1) Candidatos por transação: fornecedor/termos suspeitos e/ou valor alto
    tx_candidates = df[(df["_amount_num"] >= 1000) | (df["_desc_norm"].str.contains("tech solutions|wcs supplies", na=False))].copy()
    tx_candidates = tx_candidates.head(10)

    # 2) Candidatos por email: termos de fraude
    email_candidates = []
    for e in emails:
        blob = f"{e.assunto}\n{e.mensagem}".lower()
        hits = [t for t in FRAUD_EMAIL_TERMS if t in blob]
        if hits:
            email_candidates.append((len(hits), e, hits))
    email_candidates.sort(key=lambda x: x[0], reverse=True)
    email_top = email_candidates[:8]

    # monta contexto pro LLM cruzar
    tx_text = "\n".join([f"[tx_{i}] {row.to_dict()}" for i, (_, row) in enumerate(tx_candidates.iterrows())])
    em_text = "\n\n".join([
        f"[email_{e.idx}] De: {e.de} | Assunto: {e.assunto}\nTrecho: {e.mensagem[:280].replace(chr(10),' ')}"
        for _, e, _ in email_top
    ])

    policy = query_policy("regras de compliance sobre fraude, reembolsos indevidos, uso de cartão corporativo, aprovações")

    system = (
        "Você é um auditor antifraude. Você receberá um conjunto de transações candidatas e um conjunto de emails. "
        "Seu trabalho é apontar quais transações têm forte evidência contextual de fraude nos emails. "
        "Só marque como fraude se houver linguagem explícita de encobrimento/mascaramento/desvio. "
        "Se não houver evidência suficiente, marque como inconclusivo."
    )
    user = (
        f"Transações candidatas:\n{tx_text}\n\n"
        f"Emails candidatos:\n{em_text}\n\n"
        f"Trechos da política (para referência):\n{policy['answer']}\n\n"
        "Responda em JSON com uma lista 'casos', cada caso contendo: tx_id, email_ids, conclusao (fraude provável / inconclusivo), justificativa_curta."
    )

    result = chat(system, user)

    return {
        "llm_result": result,
        "tx_candidates": [r.to_dict() for _, r in tx_candidates.iterrows()],
        "email_candidates": [
            {
                "email_id": f"email_{e.idx}",
                "de": e.de,
                "assunto": e.assunto,
                "trecho": e.mensagem[:280].replace("\n", " ") + ("..." if len(e.mensagem) > 280 else "")
            }
            for _, e, _ in email_top
        ],
        "policy_evidence": policy
    }
