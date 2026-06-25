from pathlib import Path
import pandas as pd

from src.config import settings
from src.utils.logger import logger


def extract_movies_from_csv(file_path: Path | None = None) -> pd.DataFrame:
    if file_path is None:
        file_path = settings.DATA_DIR / "sample" / "sample_movies.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    logger.info("Reading CSV from %s", file_path)
    return pd.read_csv(file_path)
