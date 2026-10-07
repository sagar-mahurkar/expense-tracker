from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

from app.errors.exceptions import AppError


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

    @app.errorhandler(NotFound)
    def handle_not_found(error: NotFound):
        return (
            jsonify(
                {
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Resource not found",
                    }
                }
            ),
            404,
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
