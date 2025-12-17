from dataclasses import dataclass
from typing import List

@dataclass
class Evidence:
    source: str
    ref: str
    quote: str

def format_evidence(evs: List[Evidence]) -> str:
    lines = []
    for e in evs:
        q = e.quote.strip().replace("\n", " ")
        if len(q) > 220:
            q = q[:220] + "..."
        lines.append(f"- [{e.source}] ({e.ref}) \"{q}\"")
    return "\n".join(lines)
