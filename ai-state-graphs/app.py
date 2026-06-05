"""
ai-state-graphs — Flask dashboard comparing AI model benchmark scores.
"""

from __future__ import annotations

import logging
import os
import sys

from flask import Flask, abort, jsonify, render_template

from data_fetcher import get_benchmarks, get_model_details, get_model_list

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", models=get_model_list())

    @app.route("/api/benchmarks")
    def api_benchmarks():
        return jsonify(get_benchmarks())

    @app.route("/api/model/<path:model_id>")
    def api_model(model_id: str):
        detail = get_model_details(model_id)
        if detail is None:
            abort(404)
        return jsonify(detail)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        log.exception("Internal server error")
        return jsonify({"error": "internal server error"}), 500

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    create_app().run(host="0.0.0.0", port=port, debug=debug)
