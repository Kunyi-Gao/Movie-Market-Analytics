from pathlib import Path
import pandas as pd

from src.config import settings
from src.utils.logger import logger

REQUIRED_COLUMNS = [
    "title", "year", "region", "genre", "rating", "vote_count", "director",
    "douban_id", "url", "cover_url", "actors", "duration", "language", "summary",
]


def clean_text(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text if text else None


def split_multi_value(value) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    for sep in ["/", "|", ";", "，", ","]:
        text = text.replace(sep, ",")
    return sorted({part.strip() for part in text.split(",") if part.strip()})


def clean_movies_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    before = len(df)
    df = df.drop_duplicates()
    logger.info("Removed %s duplicate rows", before - len(df))

    df = df.dropna(subset=["title", "year", "director"])

    text_columns = ["title", "region", "genre", "director", "douban_id", "url", "cover_url", "actors", "language", "summary"]
    for col in text_columns:
        df[col] = df[col].apply(clean_text)

    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce").fillna(0).astype(int)
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").fillna(0).astype(int)

    df = df.dropna(subset=["year", "rating"])
    df = df[(df["rating"] >= 0) & (df["rating"] <= 10)]

    df["popularity_score"] = (df["rating"] * df["vote_count"]).round(2)
    df = df.rename(columns={"year": "release_year", "region": "country"})

    return df.reset_index(drop=True)


def save_processed_csv(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = settings.PROCESSED_DATA_DIR / "movies_processed.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Saved processed data to %s", output_path)
    return output_path
