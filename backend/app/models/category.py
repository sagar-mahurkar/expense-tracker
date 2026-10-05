from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from flask_sqlalchemy.model import Model
from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


if TYPE_CHECKING:
    BaseModel = Model
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