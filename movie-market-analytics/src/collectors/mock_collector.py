from pathlib import Path
import shutil

from src.config import settings
from src.utils.logger import logger


def collect_sample_data() -> Path:
    """Simulate a collector by copying sample data into data/raw."""
    source = settings.DATA_DIR / "sample" / "sample_movies.csv"
    target = settings.RAW_DATA_DIR / "douban_movies_raw.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, target)
    logger.info("Mock collected data to %s", target)
    return target


if __name__ == "__main__":
    collect_sample_data()
