from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Settings:
    data_dir: Path = BASE_DIR / "data"
    policy_path: Path = data_dir / "politica_compliance.txt"
    emails_path: Path = data_dir / "emails_internos.txt"
    tx_path: Path = data_dir / "transacoes_bancarias.csv"

    # index dirs
    index_dir: Path = BASE_DIR / "indexes"
    policy_index_dir: Path = index_dir / "policy"
    emails_index_dir: Path = index_dir / "emails"

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

settings = Settings()
