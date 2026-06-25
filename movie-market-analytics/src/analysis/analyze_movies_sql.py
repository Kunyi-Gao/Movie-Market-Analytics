from pathlib import Path

from src.config import settings
from src.db.mysql_helper import MySQLHelper
from src.utils.logger import logger


def print_section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_sql_file(path: Path) -> None:
    db = MySQLHelper()
    sql = path.read_text(encoding="utf-8")
    rows = db.fetch_all(sql)
    print_section(path.stem.replace("_", " ").title())
    for row in rows:
        print(row)


def main() -> None:
    sql_dir = settings.PROJECT_ROOT / "sql" / "analysis"
    if not sql_dir.exists():
        logger.error("SQL analysis directory not found: %s", sql_dir)
        return
    for path in sorted(sql_dir.glob("*.sql")):
        run_sql_file(path)


if __name__ == "__main__":
    main()
