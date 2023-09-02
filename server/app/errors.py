from flask import jsonify
from app import app, db
import logging


class ApplicationError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


# Error Handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"message": "Bad request"}), 400


@app.errorhandler(401)
def unauthorized(e):
    logging.error("Unauthorized request")
    return jsonify({"message": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found", "code": 404}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "An internal error occurred", "code": 500}), 500


@app.errorhandler(ValueError)
def value_error(error):
    return jsonify({"error": str(error), "code": 400}), 400


@app.errorhandler(ApplicationError)
def handle_application_error(error):
    return jsonify({"error": str(error), "code": error.code}), error.code
