from datetime import date
from uuid import UUID

from sqlalchemy import func, select

from app.extensions import db
from app.models.transaction import Transaction


def find_transactions_by_user(
    user_id: UUID,
    transaction_type: str | None = None,
    category_id: UUID | None = None,
    search: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Transaction], int]:

    filters = [
        Transaction.user_id == user_id,
    ]

    if transaction_type is not None:
        filters.append(Transaction.type == transaction_type)

    if category_id is not None:
        filters.append(Transaction.category_id == category_id)

    if search is not None:
        filters.append(
            Transaction.description.ilike(f"%{search}%")
        )

    if start_date is not None:
        filters.append(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        filters.append(
            Transaction.transaction_date <= end_date
        )

    count_statement = (
        select(func.count())
        .select_from(Transaction)
        .where(*filters)
    )

    total_count = db.session.scalar(count_statement) or 0

    statement = (
        select(Transaction)
        .where(*filters)
        .order_by(Transaction.transaction_date.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    transactions = list(db.session.scalars(statement).all())

    return transactions, total_count


def find_transaction_by_id(
    transaction_id: UUID,
    user_id: UUID,
) -> Transaction | None:
    statement = select(Transaction).where(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id,
    )

    return db.session.scalar(statement)


def create_transaction(
    user_id: UUID,
    category_id: UUID,
    transaction_type: str,
    amount,
    description: str | None,
    transaction_date: date,
) -> Transaction:
    transaction = Transaction()
    transaction.user_id = user_id
    transaction.category_id = category_id
    transaction.type = transaction_type
    transaction.amount = amount
    transaction.description = description
    transaction.transaction_date = transaction_date

    db.session.add(transaction)
    db.session.flush()

    return transaction


def update_transaction(
    transaction: Transaction,
    category_id: UUID,
    transaction_type: str,
    amount,
    description: str | None,
    transaction_date: date,
) -> Transaction:
    transaction.category_id = category_id
    transaction.type = transaction_type
    transaction.amount = amount
    transaction.description = description
    transaction.transaction_date = transaction_date

    db.session.flush()

    return transaction


def delete_transaction(transaction: Transaction) -> None:
    db.session.delete(transaction)
    db.session.flush()
