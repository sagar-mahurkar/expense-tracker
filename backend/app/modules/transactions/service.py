from uuid import UUID

from app.errors.exceptions import NotFoundError
from app.extensions import db
from app.modules.categories.repository import find_category_by_id
from app.modules.transactions.repository import (
    create_transaction,
    delete_transaction,
    find_transaction_by_id,
    find_transactions_by_user,
    update_transaction,
)


def list_user_transactions(
    user_id: UUID,
    transaction_type: str | None = None,
    category_id: UUID | None = None,
    search: str | None = None,
    start_date=None,
    end_date=None,
    page: int = 1,
    per_page: int = 20,
):
    return find_transactions_by_user(
        user_id=user_id,
        transaction_type=transaction_type,
        category_id=category_id,
        search=search,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page,
    )

def get_transaction(
    transaction_id: UUID,
    user_id: UUID,
):
    transaction = find_transaction_by_id(
        transaction_id=transaction_id,
        user_id=user_id,
    )

    if transaction is None:
        raise NotFoundError("Transaction not found")

    return transaction


def create_user_transaction(
    user_id: UUID,
    category_id: UUID,
    transaction_type: str,
    amount,
    description,
    transaction_date,
):
    category = find_category_by_id(
        category_id=category_id,
        user_id=user_id,
    )

    if category is None:
        raise NotFoundError("Category not found")

    try:
        transaction = create_transaction(
            user_id=user_id,
            category_id=category_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            transaction_date=transaction_date,
        )

        db.session.commit()

        return transaction
    except Exception:
        db.session.rollback()
        raise


def update_user_transaction(
    transaction_id: UUID,
    user_id: UUID,
    category_id: UUID,
    transaction_type: str,
    amount,
    description,
    transaction_date,
):
    transaction = get_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
    )

    category = find_category_by_id(
        category_id=category_id,
        user_id=user_id,
    )

    if category is None:
        raise NotFoundError("Category not found")

    try:
        transaction = update_transaction(
            transaction=transaction,
            category_id=category_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            transaction_date=transaction_date,
        )

        db.session.commit()

        return transaction
    except Exception:
        db.session.rollback()
        raise


def delete_user_transaction(
    transaction_id: UUID,
    user_id: UUID,
):
    transaction = get_transaction(
        transaction_id=transaction_id,
        user_id=user_id,
    )

    try:
        delete_transaction(transaction)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
