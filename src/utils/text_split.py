from dataclasses import dataclass
from typing import List

@dataclass
class Chunk:
    id: str
    text: str
    start: int
    end: int
    source: str

def simple_chunk(text: str, source: str, chunk_size: int = 1500, overlap: int = 200) -> List[Chunk]:
    chunks: List[Chunk] = []
    i = 0
    cid = 0
    n = len(text)
    while i < n:
        start = i
        end = min(n, i + chunk_size)
        chunk_text = text[start:end]
        chunks.append(Chunk(
            id=f"{source}_chunk_{cid}",
            text=chunk_text,
            start=start,
            end=end,
            source=source
        ))
        cid += 1
        i = end - overlap
        if i < 0:
            i = 0
        if end == n:
            break
    return chunks
