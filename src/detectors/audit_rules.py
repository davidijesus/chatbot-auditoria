import pandas as pd
from typing import Dict, List
from src.ingest.load_transactions import load_transactions_df
from src.rag.policy_rag import retrieve_policy

PROHIBITED_KEYWORDS = [
    "arma", "sniper", "munição", "drog", "vitamina", "casino", "aposta",
    "serenity", "incenso", "mágica", "algemas", "houdini", "helicóptero"
]

SUSPICIOUS_MERCHANTS = [
    "tech solutions", "wcs supplies"
]

def audit_rules() -> Dict:
    df = load_transactions_df()

    # normaliza colunas prováveis
    cols = {c.lower(): c for c in df.columns}
    amount_col = cols.get("valor") or cols.get("amount") or cols.get("value")
    desc_col = cols.get("descricao") or cols.get("descrição") or cols.get("description") or cols.get("descricao_da_transacao")
    cat_col = cols.get("categoria") or cols.get("category")
    who_col = cols.get("funcionario") or cols.get("employee") or cols.get("user")

    if not amount_col or not desc_col:
        return {
            "erro": "CSV não tem colunas mínimas esperadas (valor e descrição).",
            "colunas_encontradas": list(df.columns)
        }

    df["_desc_norm"] = df[desc_col].astype(str).str.lower()
    if cat_col:
        df["_cat_norm"] = df[cat_col].astype(str).str.lower()
    else:
        df["_cat_norm"] = ""

    violations: List[dict] = []

    # Regra 1: palavras proibidas
    for kw in PROHIBITED_KEYWORDS:
        mask = df["_desc_norm"].str.contains(kw, na=False) | df["_cat_norm"].str.contains(kw, na=False)
        for _, row in df[mask].iterrows():
            violations.append({
                "type": "proibido_por_palavra_chave",
                "keyword": kw,
                "row": row.to_dict()
            })

    # Regra 2: merchants suspeitos
    for m in SUSPICIOUS_MERCHANTS:
        mask = df["_desc_norm"].str.contains(m, na=False)
        for _, row in df[mask].iterrows():
            violations.append({
                "type": "fornecedor_suspeito",
                "merchant": m,
                "row": row.to_dict()
            })

    # Regra 3: valores muito altos (heurística)
    # (depois você pode bater com limites da política, se existir)
    mask_high = pd.to_numeric(df[amount_col], errors="coerce").fillna(0) >= 1000
    for _, row in df[mask_high].iterrows():
        violations.append({
            "type": "valor_alto",
            "threshold": 1000,
            "row": row.to_dict()
        })

    # adiciona evidência da política via RAG (pra ficar “compliance-grade”)
    enriched = []
    for v in violations[:25]:  # evita explodir a saída
        hint = f"regras de compliance sobre {v['type']} despesas proibidas limite reembolso"
        policy = retrieve_policy(hint)
        enriched.append({
            **v,
            "policy_evidence": policy
        })

    return {
        "total_violations": len(violations),
        "sample_violations": enriched,
        "note": "As regras acima são heurísticas determinísticas + evidência contextual da política. Ajuste thresholds/keywords conforme sua politica_compliance.txt."
    }
