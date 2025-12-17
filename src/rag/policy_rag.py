import json
from pathlib import Path
import numpy as np
import faiss

from src.config import settings
from src.ingest.load_policy import load_policy_text
from src.utils.text_split import simple_chunk, Chunk
from src.utils.llm import embed_texts, chat
from src.utils.citations import Evidence

META_FILE = "meta.json"

def _save_meta(chunks: list[Chunk], dir_path: Path) -> None:
    meta = [
        {"id": c.id, "text": c.text, "start": c.start, "end": c.end, "source": c.source}
        for c in chunks
    ]
    (dir_path / META_FILE).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def _load_meta(dir_path: Path) -> list[dict]:
    return json.loads((dir_path / META_FILE).read_text(encoding="utf-8"))

def build_policy_index() -> None:
    settings.policy_index_dir.mkdir(parents=True, exist_ok=True)
    text = load_policy_text()
    chunks = simple_chunk(text, source="politica_compliance", chunk_size=1500, overlap=200)

    embeddings = embed_texts([c.text for c in chunks])
    emb = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(emb.shape[1])
    faiss.normalize_L2(emb)
    index.add(emb)

    faiss.write_index(index, str(settings.policy_index_dir / "index.faiss"))
    _save_meta(chunks, settings.policy_index_dir)

def _ensure_index():
    if not (settings.policy_index_dir / "index.faiss").exists():
        build_policy_index()

def query_policy(question: str, k: int = 4) -> dict:
    _ensure_index()
    index = faiss.read_index(str(settings.policy_index_dir / "index.faiss"))
    meta = _load_meta(settings.policy_index_dir)

    q_emb = np.array(embed_texts([question]), dtype="float32")
    faiss.normalize_L2(q_emb)

    scores, ids = index.search(q_emb, k)
    retrieved = [meta[i] for i in ids[0] if i != -1]

    evidences = [
        Evidence(source=m["source"], ref=m["id"], quote=m["text"])
        for m in retrieved
    ]

    context = "\n\n".join([f"[{m['id']}]\n{m['text']}" for m in retrieved])

    system = (
        "Você é um auditor de compliance. Responda APENAS com base no contexto fornecido. "
        "Se não houver evidência no contexto, diga que não há informação suficiente."
    )
    user = (
        f"Pergunta: {question}\n\n"
        f"Contexto:\n{context}\n\n"
        "Resposta em português, objetiva, e inclua no final uma seção 'Evidências' listando os IDs usados."
    )
    answer = chat(system, user)

    return {
        "answer": answer,
        "retrieved": [
            {
                "id": m["id"],
                "source": m["source"],
                "quote": (m["text"][:250].replace("\n", " ") + ("..." if len(m["text"]) > 250 else ""))
            }
            for m in retrieved
        ]
    }

