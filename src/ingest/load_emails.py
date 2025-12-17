from src.config import settings

def load_emails_text() -> str:
    return settings.emails_path.read_text(encoding="utf-8", errors="ignore")
