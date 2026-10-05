from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from flask_sqlalchemy.model import Model
from sqlalchemy import (
    Index,
    CheckConstraint, 
    Date, 
    DateTime, 
    Numeric, 
    String, 
    Uuid, 
    ForeignKey, 
    ForeignKeyConstraint
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)

from app.models.category import Category
from app.extensions import db


if TYPE_CHECKING:
    BaseModel = Model
    from app.models.user import User
else:
    BaseModel = db.Model


class Transaction(BaseModel):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()"),
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
    )

    category_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
    )
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id", "user_id"],
            ["categories.id", "categories.user_id"],
        ),
        CheckConstraint(
            "type IN ('income', 'expense')",
            name="ck_transactions_type",
        ),
        CheckConstraint(
            "amount > 0",
            name="ck_transactions_amount_positive",
        ),
        Index(
            "idx_transactions_user_date",
            "user_id",
            "transaction_date",
        ),
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="transactions",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        primaryjoin=(
            "and_("
            "Transaction.category_id == Category.id, "
            "Transaction.user_id == Category.user_id"
            ")"
        ),
        foreign_keys="Transaction.category_id",
        back_populates="transactions",
    )