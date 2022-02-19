# Python
from typing import Optional, List


# Pydantic
from pydantic import BaseModel
from pydantic import Field


class LoanBase(BaseModel):
    loan_id: str = Field(
        ...
    )
    amount: int = Field(
        ...,
        gt=0
    )
    term: int = Field(
        ...,
        gt=0
    )
    interest_rate: float = Field(
        ...,
        ge=0.01,
        le=1.00
    )
    is_active:  bool = Field(
        default=True,
    )


class LoanCreate(LoanBase):
    pass


class Loan(LoanBase):
    id: int = Field(
        ...
    )
    client_id: int = Field(
        ...
    )

    class Config:
        orm_mode = True
