from uuid import UUID

from sqlalchemy import select

from app.extensions import db
from app.models.category import Category


def find_categories_by_user(user_id: UUID) -> list[Category]:
    statement = (
        select(Category)
        .where(Category.user_id == user_id)
        .order_by(Category.name)
    )

    return list(db.session.scalars(statement).all())


def find_category_by_id(
    category_id: UUID,
    user_id: UUID,
) -> Category | None:
    statement = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id,
    )

    return db.session.scalar(statement)


def create_category(
    user_id: UUID,
    name: str,
    category_type: str,
) -> Category:
    category = Category()
    category.user_id = user_id
    category.name = name
    category.type = category_type

    db.session.add(category)
    db.session.flush()

    return category


def delete_category(category: Category) -> None:
    db.session.delete(category)
    db.session.flush()
