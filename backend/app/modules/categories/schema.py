from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: Literal["income", "expense"]


class UpdateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: Literal["income", "expense"]


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    type: Literal["income", "expense"]
    created_at: datetime
    updated_at: datetime
