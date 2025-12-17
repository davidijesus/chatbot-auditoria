import re
from dataclasses import dataclass
from typing import List, Optional
from src.ingest.load_emails import load_emails_text

SEP = "-" * 79

@dataclass
class Email:
    idx: int
    de: str
    para: str
    data: str
    assunto: str
    mensagem: str
    raw: str

def _find_field(block: str, label: str) -> str:
    m = re.search(rf"^{label}:\s*(.*)$", block, flags=re.MULTILINE)
    return (m.group(1).strip() if m else "")

def _find_message(block: str) -> str:
    m = re.search(r"^Mensagem:\s*\n(.*)$", block, flags=re.MULTILINE | re.DOTALL)
    return (m.group(1).strip() if m else "")

def parse_emails(text: Optional[str] = None) -> List[Email]:
    if text is None:
        text = load_emails_text()

    # quebra por separadores longos
    parts = [p.strip() for p in text.split(SEP) if p.strip()]
    emails: List[Email] = []
    idx = 0

    for p in parts:
        # filtra cabeçalhos gerais do dump
        if p.startswith("DUMP DE SERVIDOR") or p.startswith("PERÍODO") or p.startswith("STATUS"):
            continue
        if "De:" not in p or "Assunto:" not in p:
            continue

        de = _find_field(p, "De")
        para = _find_field(p, "Para")
        data = _find_field(p, "Data")
        assunto = _find_field(p, "Assunto")
        mensagem = _find_message(p)

        emails.append(Email(
            idx=idx,
            de=de,
            para=para,
            data=data,
            assunto=assunto,
            mensagem=mensagem,
            raw=p
        ))
        idx += 1

    return emails
