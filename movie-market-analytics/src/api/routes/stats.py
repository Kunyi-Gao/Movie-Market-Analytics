from flask import Blueprint, jsonify

from src.api.utils.response import error_response, success_response
from src.db.mysql_helper import MySQLHelper
from src.utils.logger import logger

stats_bp = Blueprint("stats", __name__, url_prefix="/api/v1/stats")


def fetch(sql: str):
    return MySQLHelper().fetch_all(sql)


@stats_bp.get("/genres")
def stats_by_genre():
    try:
        sql = """
        SELECT g.genre_name, COUNT(DISTINCT m.movie_id) AS movie_count,
               ROUND(AVG(f.rating), 2) AS avg_rating, SUM(f.vote_count) AS total_votes
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
        JOIN dim_genre g ON b.genre_id = g.genre_id
        GROUP BY g.genre_name
        ORDER BY avg_rating DESC, movie_count DESC;
        """
        return jsonify(success_response(fetch(sql)))
    except Exception:
        logger.exception("Failed to load genre statistics")
        return jsonify(error_response("Unable to load genre statistics")), 500


@stats_bp.get("/years")
def stats_by_year():
    try:
        sql = """
        SELECT m.release_year, COUNT(*) AS movie_count,
               ROUND(AVG(f.rating), 2) AS avg_rating, SUM(f.vote_count) AS total_votes
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        GROUP BY m.release_year
        ORDER BY m.release_year;
        """
        return jsonify(success_response(fetch(sql)))
    except Exception:
        logger.exception("Failed to load year statistics")
        return jsonify(error_response("Unable to load year statistics")), 500


@stats_bp.get("/countries")
def stats_by_country():
    try:
        sql = """
        SELECT m.country, COUNT(*) AS movie_count,
               ROUND(AVG(f.rating), 2) AS avg_rating, SUM(f.vote_count) AS total_votes
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        GROUP BY m.country
        ORDER BY movie_count DESC, avg_rating DESC;
        """
        return jsonify(success_response(fetch(sql)))
    except Exception:
        logger.exception("Failed to load country statistics")
        return jsonify(error_response("Unable to load country statistics")), 500


@stats_bp.get("/popularity")
def stats_by_popularity():
    try:
        sql = """
        SELECT m.title, m.release_year, m.country, f.rating, f.vote_count, f.popularity_score
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        ORDER BY f.popularity_score DESC, f.rating DESC
        LIMIT 20;
        """
        return jsonify(success_response(fetch(sql)))
    except Exception:
        logger.exception("Failed to load popularity statistics")
        return jsonify(error_response("Unable to load popularity statistics")), 500
