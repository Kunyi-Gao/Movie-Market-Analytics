from flask import Flask, jsonify, send_file
from werkzeug.exceptions import HTTPException

from src.api.routes.genres import genres_bp
from src.api.routes.movies import movies_bp, predict_bp
from src.api.routes.stats import stats_bp
from src.api.utils.response import error_response, success_response
from src.config import settings
from src.utils.logger import logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(movies_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(predict_bp)

    @app.get("/api/v1/health")
    def health_check():
        return jsonify(success_response({"status": "ok"}))

    @app.get("/api/v1/visuals/<path:name>")
    def get_visual(name: str):
        file_path = settings.FIGURE_DIR / name
        if not file_path.exists() or file_path.suffix.lower() != ".png":
            return jsonify(error_response("Visual not found")), 404
        return send_file(file_path, mimetype="image/png")

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        response = error_response(error.description or "A request error occurred")
        return jsonify(response), error.code or 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):
        logger.exception("Unhandled exception during request")
        return jsonify(error_response("An internal server error occurred")), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=settings.FLASK_DEBUG, port=5000)
