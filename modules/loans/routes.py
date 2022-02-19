# Python
from typing import List


# FastAPI
from fastapi import Depends
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import status, Response
from fastapi import HTTPException


# ConfigDB
from config.db import SessionLocal


# SqlAlchemy
from sqlalchemy.orm import Session

# Schemas
from . import schemas


# Business Logig
from . import utils


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get(path="/loans/",
            response_model=List[schemas.Loan],
            status_code=status.HTTP_200_OK,
            tags=["Loans"]
            )
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Get all Loans.

    This path operation retrive all loans in the app.

    Returns a list json with the basic client information.
    * id: UUID.
    * loan_id: str.
    * amount: integer.
    * term: integer.
    * interest_rate: float.
    * is_active: boolean.
    '''
    items = utils.get_loans(db, skip=skip, limit=limit)
    return items


@router.get("/client/{client_id}/loans/{id}",
            response_model=schemas.Loan,
            status_code=status.HTTP_200_OK,
            tags=["Loans"])
def get_loan_for_client(client_id: int = Path(...),
                        id: int = Path(...),
                        db: Session = Depends(get_db)
                        ):
    '''
    Get Loan for a client.

    This path operation retrive a loan for a client in the app.

    Returns a json with the basic client information.
    * id: UUID.
    * loan_id: str.
    * amount: integer.
    * term: integer.
    * interest_rate: float.
    * is_active: boolean.
    '''
    db_loan = utils.get_loan_for_client(
        db=db, client_id=client_id, id=id)

    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"this loan {id}, not Exists!."
        )

    return db_loan


@router.post(path="/client/{client_id}/loans/",
             response_model=schemas.Loan,
             status_code=status.HTTP_201_CREATED,
             tags=["Loans"]
             )
def create_loan_for_client(
    client_id: int = Path(...),
    loan: schemas.LoanCreate = Body(...),
    db: Session = Depends(get_db)
):
    '''
    Create a Loan.

    This path operation create a LOAN in the app.

    Parameters:
    * Reqguest body parameter.
        * client_id: client_id.
        * loan: LoanCreate.

    Returns a json with the basic client information.
    * id: UUID.
    * loan_id: str.
    * amount: integer.
    * term: integer.
    * interest_rate: float.
    * is_active: boolean.
    '''
    return utils.create_loan_for_client(db=db, loan=loan, client_id=client_id)


@router.put(path="/client/{client_id}/loans/{id}",
            response_model=schemas.Loan,
            status_code=status.HTTP_200_OK,
            tags=["Loans"]
            )
def update_loan_for_client(
    client_id: int = Path(...),
    id: int = Path(...),
    loan: schemas.LoanCreate = Body(...),
    db: Session = Depends(get_db)
):
    '''
    Update Loan for a client.

    This path operation update a loan for a client in the app.

    Returns a json with the basic client information.
    * id: UUID.
    * loan_id: str.
    * amount: integer.
    * term: integer.
    * interest_rate: float.
    * is_active: boolean.
    '''
    return utils.update_loan_for_client(db=db, loan=loan, client_id=client_id, id=id)


@router.delete(path="/client/{client_id}/loans/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["Loans"])
def delete_loan_for_client(client_id: int = Path(...),
                           id: int = Path(...),
                           db: Session = Depends(get_db)
                           ):
    '''
    Delete Loan for a client.

    This path operation delete a loan for a client in the app.
    '''
    flag = utils.delete_loan_for_client(db=db, client_id=client_id, id=id)

    if not flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"this loan {id}. Not Esists!."
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
