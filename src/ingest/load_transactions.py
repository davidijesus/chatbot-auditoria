import pandas as pd
from src.config import settings

def load_transactions_df() -> pd.DataFrame:
    return pd.read_csv(settings.tx_path)
