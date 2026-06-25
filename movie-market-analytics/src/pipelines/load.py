import pandas as pd

from src.db.mysql_helper import MySQLHelper
from src.pipelines.transform import split_multi_value
from src.utils.logger import logger


def load_dim_movie(df: pd.DataFrame, db: MySQLHelper) -> None:
    sql = """
    INSERT INTO dim_movie
    (douban_id, title, release_year, country, director, actors, duration, language, summary, url, cover_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        country = VALUES(country),
        actors = VALUES(actors),
        duration = VALUES(duration),
        language = VALUES(language),
        summary = VALUES(summary),
        url = VALUES(url),
        cover_url = VALUES(cover_url);
    """
    rows = [
        (
            row.get("douban_id"), row["title"], int(row["release_year"]), row.get("country"),
            row.get("director"), row.get("actors"), int(row.get("duration", 0)), row.get("language"),
            row.get("summary"), row.get("url"), row.get("cover_url"),
        )
        for _, row in df.iterrows()
    ]
    db.execute_many(sql, rows)
    logger.info("Loaded %s rows into dim_movie", len(rows))


def load_dim_genre(df: pd.DataFrame, db: MySQLHelper) -> None:
    genres = sorted({genre for value in df["genre"] for genre in split_multi_value(value)})
    sql = """
    INSERT INTO dim_genre (genre_name)
    VALUES (%s)
    ON DUPLICATE KEY UPDATE genre_name = VALUES(genre_name);
    """
    db.execute_many(sql, [(genre,) for genre in genres])
    logger.info("Loaded %s rows into dim_genre", len(genres))


def fetch_movie_id_map(db: MySQLHelper) -> dict[tuple[str, int, str], int]:
    rows = db.fetch_all("SELECT movie_id, title, release_year, director FROM dim_movie;")
    return {(r["title"], int(r["release_year"]), r["director"]): int(r["movie_id"]) for r in rows}


def fetch_genre_id_map(db: MySQLHelper) -> dict[str, int]:
    rows = db.fetch_all("SELECT genre_id, genre_name FROM dim_genre;")
    return {r["genre_name"]: int(r["genre_id"]) for r in rows}


def load_fact_movie_rating(df: pd.DataFrame, db: MySQLHelper) -> None:
    movie_map = fetch_movie_id_map(db)
    sql = """
    INSERT INTO fact_movie_rating (movie_id, rating, vote_count, popularity_score)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        rating = VALUES(rating),
        vote_count = VALUES(vote_count),
        popularity_score = VALUES(popularity_score),
        collected_at = CURRENT_TIMESTAMP;
    """
    rows = []
    for _, row in df.iterrows():
        movie_id = movie_map[(row["title"], int(row["release_year"]), row["director"])]
        rows.append((movie_id, float(row["rating"]), int(row["vote_count"]), float(row["popularity_score"])))
    db.execute_many(sql, rows)
    logger.info("Loaded %s rows into fact_movie_rating", len(rows))


def load_bridge_movie_genre(df: pd.DataFrame, db: MySQLHelper) -> None:
    movie_map = fetch_movie_id_map(db)
    genre_map = fetch_genre_id_map(db)
    sql = """
    INSERT IGNORE INTO bridge_movie_genre (movie_id, genre_id)
    VALUES (%s, %s);
    """
    rows = []
    for _, row in df.iterrows():
        movie_id = movie_map[(row["title"], int(row["release_year"]), row["director"])]
        for genre in split_multi_value(row["genre"]):
            rows.append((movie_id, genre_map[genre]))
    db.execute_many(sql, rows)
    logger.info("Loaded %s rows into bridge_movie_genre", len(rows))


def load_all(df: pd.DataFrame) -> None:
    db = MySQLHelper()
    load_dim_movie(df, db)
    load_dim_genre(df, db)
    load_fact_movie_rating(df, db)
    load_bridge_movie_genre(df, db)
