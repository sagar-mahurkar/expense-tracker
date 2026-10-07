from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateTransactionRequest(BaseModel):
    category_id: UUID
    type: Literal["income", "expense"]
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    description: str | None = Field(default=None, max_length=500)
    transaction_date: date


class UpdateTransactionRequest(BaseModel):
    category_id: UUID
    type: Literal["income", "expense"]
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    description: str | None = Field(default=None, max_length=500)
    transaction_date: date


class TransactionResponse(BaseModel):
    id: UUID
    category_id: UUID
    type: Literal["income", "expense"]
    amount: Decimal
    description: str | None
    transaction_date: date
    created_at: datetime
    updated_at: datetime
