from decimal import Decimal

from pydantic import BaseModel


class SummaryResponse(BaseModel):
    income: Decimal
    expense: Decimal
    balance: Decimal


class MonthlySummaryResponse(BaseModel):
    year: int
    month: int
    income: Decimal
    expense: Decimal
    balance: Decimal