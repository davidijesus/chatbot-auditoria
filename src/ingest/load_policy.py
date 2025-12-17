from src.config import settings

def load_policy_text() -> str:
    return settings.policy_path.read_text(encoding="utf-8", errors="ignore")
