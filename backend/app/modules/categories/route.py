from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.categories.schema import CreateCategoryRequest
from app.modules.categories.service import (
    create_user_category,
    delete_user_category,
    get_category,
    list_categories,
)
from app.schemas.validation import validate_request


categories_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/api/v1/categories",
)


@categories_bp.get("")
@jwt_required()
def list_categories_route():
    user_id = UUID(get_jwt_identity())

    categories = list_categories(user_id=user_id)

    return jsonify(
        {
            "data": [
                {
                    "id": str(category.id),
                    "name": category.name,
                    "type": category.type,
                    "created_at": category.created_at.isoformat(),
                    "updated_at": category.updated_at.isoformat(),
                }
                for category in categories
            ]
        }
    ), 200


@categories_bp.post("")
@jwt_required()
def create_category_route():
    request_data = validate_request(
        request,
        CreateCategoryRequest,
    )

    user_id = UUID(get_jwt_identity())

    category = create_user_category(
        user_id=user_id,
        name=request_data.name,
        category_type=request_data.type,
    )

    return jsonify(
        {
            "data": {
                "id": str(category.id),
                "name": category.name,
                "type": category.type,
                "created_at": category.created_at.isoformat(),
                "updated_at": category.updated_at.isoformat(),
            }
        }
    ), 201


@categories_bp.get("/<uuid:category_id>")
@jwt_required()
def get_category_route(category_id: UUID):
    user_id = UUID(get_jwt_identity())

    category = get_category(
        category_id=category_id,
        user_id=user_id,
    )

    return jsonify(
        {
            "data": {
                "id": str(category.id),
                "name": category.name,
                "type": category.type,
                "created_at": category.created_at.isoformat(),
                "updated_at": category.updated_at.isoformat(),
            }
        }
    ), 200


@categories_bp.delete("/<uuid:category_id>")
@jwt_required()
def delete_category_route(category_id: UUID):
    user_id = UUID(get_jwt_identity())

    delete_user_category(
        category_id=category_id,
        user_id=user_id,
    )

    return "", 204
