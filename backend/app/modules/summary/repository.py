from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select

from app.extensions import db
from app.models.transaction import Transaction


def get_user_summary(user_id: UUID) -> tuple[Decimal, Decimal]:
    statement = select(
        func.coalesce(
            func.sum(Transaction.amount).filter(
                Transaction.type == "income"
            ),
            0,
        ),
        func.coalesce(
            func.sum(Transaction.amount).filter(
                Transaction.type == "expense"
            ),
            0,
        ),
    ).where(Transaction.user_id == user_id)

    income, expense = db.session.execute(statement).one()

    return Decimal(income), Decimal(expense)


def get_user_monthly_summary(
    user_id: UUID,
    start_date: date,
    end_date: date,
) -> tuple[Decimal, Decimal]:
    statement = select(
        func.coalesce(
            func.sum(Transaction.amount).filter(
                Transaction.type == "income"
            ),
            0,
        ),
        func.coalesce(
            func.sum(Transaction.amount).filter(
                Transaction.type == "expense"
            ),
            0,
        ),
    ).where(
        Transaction.user_id == user_id,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date < end_date,
    )

    income, expense = db.session.execute(statement).one()

    return Decimal(income), Decimal(expense)
