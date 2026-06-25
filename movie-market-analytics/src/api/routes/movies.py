from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

import pandas as pd
import joblib

from src.api.utils.response import error_response, success_response
from src.config import settings
from src.db.mysql_helper import MySQLHelper
from src.ml.features import build_features
from src.utils.logger import logger

movies_bp = Blueprint("movies", __name__, url_prefix="/api/v1/movies")
predict_bp = Blueprint("predict", __name__, url_prefix="/api/v1/predict")

ALLOWED_SORT_FIELDS = {
    "rating": "f.rating",
    "vote_count": "f.vote_count",
    "year": "m.release_year",
    "title": "m.title",
    "popularity": "f.popularity_score",
}


def parse_int(value: str | None, name: str, default: int | None = None, min_value: int | None = None) -> int | None:
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise BadRequest(f"Invalid {name}: {value}")
    if min_value is not None and parsed < min_value:
        raise BadRequest(f"{name.capitalize()} must be at least {min_value}")
    return parsed


@movies_bp.get("")
def list_movies():
    try:
        page = parse_int(request.args.get("page"), "page", default=1, min_value=1)
        page_size = parse_int(request.args.get("page_size"), "page_size", default=20, min_value=1)
        if page_size is None:
            page_size = 20
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size

        genre = request.args.get("genre")
        country = request.args.get("country")
        director = request.args.get("director")
        year_min = parse_int(request.args.get("year_min"), "year_min")
        year_max = parse_int(request.args.get("year_max"), "year_max")
        sort_by = request.args.get("sort_by", "rating")
        order = request.args.get("order", "desc").lower()

        sort_col = ALLOWED_SORT_FIELDS.get(sort_by, "f.rating")
        order_sql = "ASC" if order == "asc" else "DESC"

        where = ["1=1"]
        params = []
        if genre:
            where.append("g.genre_name = %s")
            params.append(genre)
        if country:
            where.append("m.country = %s")
            params.append(country)
        if director:
            where.append("m.director = %s")
            params.append(director)
        if year_min is not None:
            where.append("m.release_year >= %s")
            params.append(year_min)
        if year_max is not None:
            where.append("m.release_year <= %s")
            params.append(year_max)

        where_sql = " AND ".join(where)
        db = MySQLHelper()

        count_sql = f"""
        SELECT COUNT(DISTINCT m.movie_id) AS total
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        LEFT JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
        LEFT JOIN dim_genre g ON b.genre_id = g.genre_id
        WHERE {where_sql};
        """
        total = db.fetch_one(count_sql, params)["total"]

        sql = f"""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.country,
            m.director,
            GROUP_CONCAT(DISTINCT g.genre_name ORDER BY g.genre_name SEPARATOR ', ') AS genres,
            f.rating,
            f.vote_count,
            f.popularity_score
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        LEFT JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
        LEFT JOIN dim_genre g ON b.genre_id = g.genre_id
        WHERE {where_sql}
        GROUP BY m.movie_id, f.rating_id
        ORDER BY {sort_col} {order_sql}
        LIMIT %s OFFSET %s;
        """
        rows = db.fetch_all(sql, params + [page_size, offset])
        return jsonify(success_response(rows, {"page": page, "page_size": page_size, "total": total}))
    except BadRequest:
        raise
    except Exception:
        logger.exception("Failed to list movies")
        return jsonify(error_response("Unable to retrieve movie list")), 500


@movies_bp.get("/<int:movie_id>")
def get_movie(movie_id: int):
    try:
        db = MySQLHelper()
        sql = """
        SELECT
            m.*,
            GROUP_CONCAT(DISTINCT g.genre_name ORDER BY g.genre_name SEPARATOR ', ') AS genres,
            f.rating,
            f.vote_count,
            f.popularity_score
        FROM dim_movie m
        JOIN fact_movie_rating f ON m.movie_id = f.movie_id
        LEFT JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
        LEFT JOIN dim_genre g ON b.genre_id = g.genre_id
        WHERE m.movie_id = %s
        GROUP BY m.movie_id, f.rating_id;
        """
        movie = db.fetch_one(sql, (movie_id,))
        if not movie:
            return jsonify(error_response("Movie not found")), 404
        return jsonify(success_response(movie))
    except Exception:
        logger.exception("Failed to retrieve movie %s", movie_id)
        return jsonify(error_response("Unable to retrieve movie details")), 500


def load_prediction_model():
    model_path = settings.OUTPUT_DIR / "model.pkl"
    if not model_path.exists():
        logger.error("Prediction model not found at %s", model_path)
        raise FileNotFoundError("Trained model not found. Run `python -m src.ml.train` first.")
    return joblib.load(model_path)


@predict_bp.post("/rating")
def predict_rating_api():
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            raise BadRequest("A JSON payload is required")

        if isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list):
            raise BadRequest("Request body must be a JSON object or an array of objects")

        df = pd.DataFrame(payload)
        if df.empty:
            raise BadRequest("Request body must contain at least one record")

        required_columns = ["genres", "release_year", "duration", "vote_count", "country"]
        missing_columns = [column for column in required_columns if column not in df.columns]
        if missing_columns:
            raise BadRequest(f"Missing required features: {', '.join(missing_columns)}")

        model = load_prediction_model()
        X, _, _ = build_features(df)
        predictions = model.predict(X)

        return jsonify(success_response({"predictions": predictions.tolist()}))
    except BadRequest:
        raise
    except FileNotFoundError as err:
        logger.error("Prediction error: %s", err)
        return jsonify(error_response(str(err))), 500
    except Exception:
        logger.exception("Failed to predict rating")
        return jsonify(error_response("Unable to generate prediction")), 500
