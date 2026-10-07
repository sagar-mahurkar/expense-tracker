from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.summary.service import (
    get_monthly_summary,
    get_summary,
)


summary_bp = Blueprint(
    "summary",
    __name__,
    url_prefix="/api/v1/summary",
)


def summary_response(summary: dict) -> dict:
    return {
        "income": str(summary["income"]),
        "expense": str(summary["expense"]),
        "balance": str(summary["balance"]),
    }


@summary_bp.get("")
@jwt_required()
def summary():
    user_id = UUID(get_jwt_identity())

    data = get_summary(user_id)

    return jsonify({
        "data": summary_response(data)
    }), 200


@summary_bp.get("/monthly")
@jwt_required()
def monthly_summary():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if year is None or month is None:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Year and month are required",
            }
        }), 400

    user_id = UUID(get_jwt_identity())

    data = get_monthly_summary(
        user_id=user_id,
        year=year,
        month=month,
    )

    response_data = {
        "year": data["year"],
        "month": data["month"],
        "income": str(data["income"]),
        "expense": str(data["expense"]),
        "balance": str(data["balance"]),
    }

    return jsonify({
        "data": response_data
    }), 200
