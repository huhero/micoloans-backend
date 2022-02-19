# Python
from typing import Optional, List


# Pydantic
from pydantic import BaseModel
from pydantic import Field


# Schemas
from ..loans import schemas


class ClientBase(BaseModel):
    nit: str = Field(
        ...
    )
    name: str = Field(
        ...
    )
    is_active:  bool = Field(
        default=True,
    )


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    loans: List[schemas.Loan] = []

    class Config:
        orm_mode = True
