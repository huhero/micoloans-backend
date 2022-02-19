# Python
from typing import Optional, List


# Pydantic
from pydantic import BaseModel
from pydantic import Field


# Schemas
from ..loans import schemas


class Amortization(BaseModel):
    number: int
    amortization_amount: float
    interest: float
    principal: float
    balance: float
