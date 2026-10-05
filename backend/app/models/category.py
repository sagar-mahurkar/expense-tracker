from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from flask_sqlalchemy.model import Model
from sqlalchemy import (
    CheckConstraint, 
    DateTime, 
    String, 
    Uuid, 
    ForeignKey, 
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)

from app.extensions import db


if TYPE_CHECKING:
    BaseModel = Model
    from app.models.transaction import Transaction
    from app.models.user import User
else:
    BaseModel = db.Model


class Category(BaseModel):
    __tablename__ = "categories"

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

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(10),
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
        UniqueConstraint(
            "id",
            "user_id",
            name="uq_categories_id_user_id",
        ),
        UniqueConstraint(
            "user_id",
            "name",
            "type",
            name="uq_categories_user_name_type",
        ),
        CheckConstraint(
            "type IN ('income', 'expense')",
            name="ck_categories_type",
        ),
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="categories",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        primaryjoin=(
            "and_("
            "Transaction.category_id == Category.id, "
            "Transaction.user_id == Category.user_id"
            ")"
        ),
        foreign_keys="Transaction.category_id",
        back_populates="category",
    )