from flask import Blueprint, jsonify, request

from app.modules.auth.schema import RegisterRequest
from app.modules.auth.service import register_user
from app.schemas.validation import validate_request

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/register")
def register():
    request_data = validate_request(
        request,
        RegisterRequest,
    )

    user = register_user(
        name=request_data.name,
        email=request_data.email,
        password=request_data.password,
    )

    return (
        jsonify(
            {
                "data": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                }
            }
        ),
        201,
    )

from app.modules.auth.schema import LoginRequest
from app.modules.auth.service import login_user


@auth_bp.post("/login")
def login():
    request_data = validate_request(
        request,
        LoginRequest,
    )

    user, access_token = login_user(
        email=request_data.email,
        password=request_data.password,
    )

    return (
        jsonify(
            {
                "data": {
                    "access_token": access_token,
                    "user": {
                        "id": str(user.id),
                        "name": user.name,
                        "email": user.email,
                    },
                }
            }
        ),
        200,
    )
