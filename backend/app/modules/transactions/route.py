from datetime import date
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.transactions.schema import (
    CreateTransactionRequest,
    UpdateTransactionRequest,
)
from app.modules.transactions.service import (
    create_user_transaction,
    delete_user_transaction,
    get_transaction,
    list_user_transactions,
    update_user_transaction,
)
from app.schemas.validation import validate_request


transactions_bp = Blueprint(
    "transactions",
    __name__,
    url_prefix="/api/v1/transactions",
)


def transaction_response(transaction):
    return {
        "id": str(transaction.id),
        "category_id": str(transaction.category_id),
        "type": transaction.type,
        "amount": str(transaction.amount),
        "description": transaction.description,
        "transaction_date": transaction.transaction_date.isoformat(),
        "created_at": transaction.created_at.isoformat(),
        "updated_at": transaction.updated_at.isoformat(),
    }


@transactions_bp.get("")
@jwt_required()
def list_transactions_route():
    user_id = UUID(get_jwt_identity())

    transaction_type = request.args.get("type")

    category_id_value = request.args.get("category_id")
    category_id = (
        UUID(category_id_value)
        if category_id_value
        else None
    )
    
    search = request.args.get("search")

    start_date_value = request.args.get("start_date")
    start_date = (
        date.fromisoformat(start_date_value)
        if start_date_value
        else None
    )

    end_date_value = request.args.get("end_date")
    end_date = (
        date.fromisoformat(end_date_value)
        if end_date_value
        else None
    )

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=20, type=int)

    transactions, total_count = list_user_transactions(
        user_id=user_id,
        transaction_type=transaction_type,
        category_id=category_id,
        search=search,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )
    
    total_pages = (
        (total_count + per_page - 1) // per_page
        if total_count > 0
        else 0
    )

    return jsonify(
        {
            "data": [
                transaction_response(transaction)
                for transaction in transactions
            ],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_count,
                "total_pages": total_pages,
            },
        }
    ), 200

@transactions_bp.post("")
@jwt_required()
def create_transaction_route():
    request_data = validate_request(
        request,
        CreateTransactionRequest,
    )

    user_id = UUID(get_jwt_identity())

    transaction = create_user_transaction(
        user_id=user_id,
        category_id=request_data.category_id,
        transaction_type=request_data.type,
        amount=request_data.amount,
        description=request_data.description,
        transaction_date=request_data.transaction_date,
    )

    return jsonify(
        {
            "data": transaction_response(transaction)
        }
    ), 201


@transactions_bp.get("/<uuid:transaction_id>")
@jwt_required()
def get_transaction_route(transaction_id: UUID):
    user_id = UUID(get_jwt_identity())

    transaction = get_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
    )

    return jsonify(
        {
            "data": transaction_response(transaction)
        }
    ), 200


@transactions_bp.put("/<uuid:transaction_id>")
@jwt_required()
def update_transaction_route(transaction_id: UUID):
    request_data = validate_request(
        request,
        UpdateTransactionRequest,
    )

    user_id = UUID(get_jwt_identity())

    transaction = update_user_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
        category_id=request_data.category_id,
        transaction_type=request_data.type,
        amount=request_data.amount,
        description=request_data.description,
        transaction_date=request_data.transaction_date,
    )

    return jsonify(
        {
            "data": transaction_response(transaction)
        }
    ), 200


@transactions_bp.delete("/<uuid:transaction_id>")
@jwt_required()
def delete_transaction_route(transaction_id: UUID):
    user_id = UUID(get_jwt_identity())

    delete_user_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
    )

    return "", 204
