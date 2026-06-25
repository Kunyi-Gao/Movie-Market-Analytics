from src.db.mysql_helper import MySQLHelper


def main() -> None:
    db = MySQLHelper()
    checks = {
        "dim_movie_count": "SELECT COUNT(*) AS value FROM dim_movie;",
        "missing_critical_values": """
            SELECT COUNT(*) AS value FROM dim_movie m
            JOIN fact_movie_rating f ON m.movie_id = f.movie_id
            WHERE m.title IS NULL OR m.title = '' OR m.release_year IS NULL
               OR f.rating IS NULL OR f.vote_count IS NULL;
        """,
        "invalid_rating_count": "SELECT COUNT(*) AS value FROM fact_movie_rating WHERE rating < 0 OR rating > 10;",
        "bridge_count": "SELECT COUNT(*) AS value FROM bridge_movie_genre;",
    }
    for name, sql in checks.items():
        print(f"{name}: {db.fetch_one(sql)['value']}")


if __name__ == "__main__":
    main()
