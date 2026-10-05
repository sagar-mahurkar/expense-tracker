from flask import jsonify
from flask_jwt_extended import JWTManager


def configure_jwt(jwt: JWTManager) -> None:
    @jwt.unauthorized_loader
    def handle_missing_jwt(error):
        return (
            jsonify(
                {
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Authentication required",
                    }
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def handle_invalid_jwt(error):
        return (
            jsonify(
                {
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Invalid authentication token",
                    }
                }
            ),
            401,
        )

    @jwt.expired_token_loader
    def handle_expired_jwt(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Authentication token has expired",
                    }
                }
            ),
            401,
        )
