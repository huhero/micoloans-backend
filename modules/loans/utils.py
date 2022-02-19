# SqlAlchemy
from sqlalchemy.orm import Session

# Models Schemas
from . import models

# Schemas
from . import schemas


def create_loan_for_client(db: Session, loan: schemas.LoanCreate, client_id: int):
    db_loan = models.Loan(**loan.dict(), client_id=client_id)
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loans(db: Session, skip: int = 0, limit: int = 100):
    db_loans = db.query(models.Loan).filter(
        models.Loan.is_active == True
    ).offset(skip).limit(limit).all()

    return db_loans


def get_loan_for_client(db: Session, client_id: int, id: int):
    db_loan = db.query(models.Loan).filter(
        models.Loan.id == id
    ).filter(
        models.Loan.client_id == client_id
    ).filter(
        models.Loan.is_active == True
    ).first()

    return db_loan


def get_loan_for_id(db: Session, loan_id: str):
    db_loan = db.query(models.Loan).filter(
        models.Loan.loan_id == loan_id
    ).filter(
        models.Loan.is_active == True
    ).first()

    return db_loan


def update_loan_for_client(db: Session, loan: schemas.LoanCreate, client_id: int, id: int):

    db.query(models.Loan).filter(
        models.Loan.id == id
    ).filter(
        models.Loan.client_id == client_id
    ).update(
        loan.dict()
    )
    db.commit()

    db_loan = db.query(models.Loan).filter(
        models.Loan.id == id
    ).filter(
        models.Loan.is_active == True
    ).first()

    return db_loan


def delete_loan_for_client(db: Session, client_id: int, id: int):
    flag = False
    try:
        db.query(models.Loan).filter(
            models.Loan.id == id
        ).filter(
            models.Loan.client_id == client_id
        ).update(
            {models.Loan.is_active: False}
        )
        db.commit()
        flag = True
    except:
        flag = False

    return flag
