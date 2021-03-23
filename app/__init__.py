"""Flask app factory."""
from typing import List

from flask import Flask, jsonify, Response, request

from app.database import db
from app.exceptions import ValidationError
from app.handlers import get_metrics_crossing


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuation for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/metrics", methods=["GET"])
    def metrics() -> List:
        """Returns list of dicts with artist_id and crossings of the specified value."""
        metric_value = request.args.get('metric_value', type=int)
        if not metric_value:
            raise ValidationError('metric_value should be an integer')

        crossing_metrics = get_metrics_crossing(metric_value)
        return jsonify(crossing_metrics)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error) -> Response:
        """Returns a validation error response in a generic format."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
