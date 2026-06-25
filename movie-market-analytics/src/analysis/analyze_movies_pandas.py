import pandas as pd

from src.db.mysql_helper import MySQLHelper
from src.utils.logger import logger


def load_movies_dataframe() -> pd.DataFrame:
    db = MySQLHelper()
    sql = """
    SELECT
        m.movie_id,
        m.title,
        m.release_year,
        m.country,
        GROUP_CONCAT(g.genre_name ORDER BY g.genre_name SEPARATOR ', ') AS genres,
        f.rating,
        f.vote_count,
        f.popularity_score,
        m.director,
        m.douban_id,
        m.url,
        m.cover_url,
        m.actors,
        m.duration,
        m.language,
        m.summary
    FROM dim_movie m
    JOIN fact_movie_rating f ON m.movie_id = f.movie_id
    LEFT JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
    LEFT JOIN dim_genre g ON b.genre_id = g.genre_id
    GROUP BY m.movie_id, f.rating_id;
    """
    rows = db.fetch_all(sql)
    df = pd.DataFrame(rows)
    if not df.empty:
        for col in ["rating", "vote_count", "duration", "release_year", "popularity_score"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def summarize_movies(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return {
        "total_movies": int(len(df)),
        "avg_rating": round(float(df["rating"].mean()), 2),
        "total_votes": int(df["vote_count"].sum()),
        "year_min": int(df["release_year"].min()),
        "year_max": int(df["release_year"].max()),
    }


def main() -> None:
    df = load_movies_dataframe()
    if df.empty:
        logger.warning("No movie data found. Please run the ETL pipeline first.")
        return
    logger.info("Basic summary:")
    logger.info("%s", summarize_movies(df))
    logger.info("Top rated movies:")
    logger.info("%s", df.sort_values(["rating", "vote_count"], ascending=[False, False]).head(10)[["title", "release_year", "genres", "rating", "vote_count"]])


if __name__ == "__main__":
    main()
