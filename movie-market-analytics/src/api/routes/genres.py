from flask import Blueprint, jsonify

from src.api.utils.response import error_response, success_response
from src.db.mysql_helper import MySQLHelper
from src.utils.logger import logger

genres_bp = Blueprint("genres", __name__, url_prefix="/api/v1/genres")


@genres_bp.get("")
def list_genres():
    try:
        db = MySQLHelper()
        rows = db.fetch_all("SELECT genre_id, genre_name FROM dim_genre ORDER BY genre_name;")
        return jsonify(success_response(rows))
    except Exception:
        logger.exception("Failed to fetch genres")
        return jsonify(error_response("Unable to load genres")), 500
