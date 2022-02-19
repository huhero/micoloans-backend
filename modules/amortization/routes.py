# Python
from typing import List


# FastAPI
from fastapi import Depends
from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from fastapi import status

# Schemas
from . import schemas


# Utils
from . import utils
from ..loans import utils as utils_loans


# ConfigDB
from config.db import SessionLocal


# SqlAlchemy
from sqlalchemy.orm import Session


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    path="/loan/{loan_id}/amortization",
    response_model=List[schemas.Amortization],
    status_code=status.HTTP_200_OK,
    tags=["Amortization"])
def get_amortization(loan_id: str = Path(...), db: Session = Depends(get_db)):
    '''
    Get Amortization table for a loan.

    This path operation create a client in the app.

    Parameters:
    * Reqguest path parameter.
        * loan_id: str

    Returns a list json with the basic amortization information.
    * number: int.
    * amortization_amount: float.
    * interest: float.
    * principal: float.
    * balance: float.
    '''
    db_loan = utils_loans.get_loan_for_id(db=db, loan_id=loan_id)
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"this loan {loan_id} not Exists!."
        )
    amount = db_loan.amount
    interest = db_loan.interest_rate
    term = db_loan.term
    return utils.amortization_schedule(principal=amount, interest_rate=interest, period=term)
