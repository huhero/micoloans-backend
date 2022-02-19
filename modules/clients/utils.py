# SqlAlchemy
from sqlalchemy.orm import Session


# Models Schemas
from . import models


# Schemas
from . import schemas


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(nit=client.nit, name=client.name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).filter(models.Client.is_active == True).first()


def get_client_by_nit(db: Session, nit: str):
    return db.query(models.Client).filter(models.Client.nit == nit).filter(models.Client.is_active == True).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    db_clients = db.query(models.Client).filter(
        models.Client.is_active == True
    ).offset(skip).limit(limit).all()
    return db_clients


def update_client(db: Session, client_id: int, client: schemas.ClientCreate):
    db.query(models.Client).filter(
        models.Client.id == client_id
    ).update(
        client.dict()
    )
    db.commit()

    db_client = db.query(models.Client).filter(
        models.Client.id == client_id
    ).first()
    return db_client


def delete_client(db: Session, client_id: int):
    flag = False
    try:
        db.query(models.Client).filter(
            models.Client.id == client_id
        ).update(
            {models.Client.is_active: False}
        )
        db.commit()
        flag = True
        print("si**************")
    except Exception as e:
        print("no**************")
        print(e)
        flag = False

    return flag
