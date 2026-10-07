from datetime import date
from decimal import Decimal
from uuid import UUID

from app.errors.exceptions import ValidationError
from app.modules.summary.repository import (
    get_user_monthly_summary,
    get_user_summary,
)


def get_summary(user_id: UUID) -> dict[str, Decimal]:
    income, expense = get_user_summary(user_id)

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
    }


def get_monthly_summary(
    user_id: UUID,
    year: int,
    month: int,
) -> dict[str, int | Decimal]:
    if month < 1 or month > 12:
        raise ValidationError("Month must be between 1 and 12")

    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    income, expense = get_user_monthly_summary(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "year": year,
        "month": month,
        "income": income,
        "expense": expense,
        "balance": income - expense,
    }