from pathlib import Path

from src.pipelines.extract import extract_movies_from_csv
from src.pipelines.load import load_all
from src.pipelines.transform import clean_movies_dataframe, save_processed_csv
from src.utils.logger import logger


def main(csv_path: str | None = None) -> None:
    logger.info("Movie Market v2 pipeline started")
    try:
        raw_df = extract_movies_from_csv(Path(csv_path) if csv_path else None)
        processed_df = clean_movies_dataframe(raw_df)
        save_processed_csv(processed_df)
        load_all(processed_df)
        logger.info("Movie Market v2 pipeline finished")
    except Exception:
        logger.exception("Movie pipeline failed")
        raise


if __name__ == "__main__":
    main()
