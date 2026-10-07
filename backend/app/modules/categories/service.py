from uuid import UUID

from app.errors.exceptions import NotFoundError, ValidationError
from app.extensions import db
from app.modules.categories.repository import (
    create_category,
    delete_category,
    find_categories_by_user,
    find_category_by_id,
)


def list_categories(user_id: UUID):
    return find_categories_by_user(user_id)


def get_category(category_id: UUID, user_id: UUID):
    category = find_category_by_id(
        category_id=category_id,
        user_id=user_id,
    )

    if category is None:
        raise NotFoundError("Category not found")

    return category


def create_user_category(
    user_id: UUID,
    name: str,
    category_type: str,
):
    existing_categories = find_categories_by_user(user_id)

    for category in existing_categories:
        if category.name == name and category.type == category_type:
            raise ValidationError("Category already exists")

    try:
        category = create_category(
            user_id=user_id,
            name=name,
            category_type=category_type,
        )
        db.session.commit()
        return category
    except Exception:
        db.session.rollback()
        raise


def delete_user_category(
    category_id: UUID,
    user_id: UUID,
) -> None:
    category = get_category(
        category_id=category_id,
        user_id=user_id,
    )

    try:
        delete_category(category)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
