from flask import Flask, jsonify

from app.errors.exceptions import AppError
from flask_jwt_extended.exceptions import JWTExtendedException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return (
            jsonify(
                {
                    "error": {
                        "code": error.code,
                        "message": error.message,
                    }
                }
            ),
            error.status_code,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        return (
            jsonify(
                {
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )
