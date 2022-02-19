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


# Utils
from . import utils


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(path="/clients/",
             response_model=schemas.Client,
             status_code=status.HTTP_201_CREATED,
             tags=["Clients"]
             )
def create_user(client: schemas.ClientCreate = Body(...), db: Session = Depends(get_db)):
    '''
    Create a Client.

    This path operation create a client in the app.

    Parameters:
    * Reqguest body parameter.
        * client: client

    Returns a list json with the basic client information.
    * id: UUID.
    * name: str.
    * is_active: boolean.
    * loans: list[loans]
    '''
    db_user = utils.get_client_by_nit(db, nit=client.nit)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nit already registered")
    return utils.create_client(db=db, client=client)


@router.get(path="/clients/",
            response_model=List[schemas.Client],
            status_code=status.HTTP_200_OK,
            tags=["Clients"]
            )
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Get all Clients.

    This path operation create a client in the app.

    Parameters:
    * Reqguest path parameter.
        * skip: int
        * limit: int

    Returns a list json with the basic client information.
    * id: UUID.
    * name: str.
    * is_active: boolean.
    * loans: list[loans]
    '''
    users = utils.get_clients(db, skip=skip, limit=limit)
    return users


@router.get(path="/clients/{client_id}",
            response_model=schemas.Client,
            status_code=status.HTTP_200_OK,
            tags=["Clients"]
            )
def read_user(client_id: int = Path(...), db: Session = Depends(get_db)):
    '''
    Get a Client.

    This path operation create a client in the app.

    Parameters:
    * Reqguest path parameter.
        * client_id: int

    Returns a json with the basic client information.
    * id: UUID.
    * name: str.
    * is_active: boolean.
    * loans: list[loans]
    '''
    db_user = utils.get_client(db, client_id=client_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Client not found")
    return db_user


@router.put(
    path="/cients/{client_id}",
    response_model=schemas.Client,
    status_code=status.HTTP_200_OK,
    tags=["Clients"])
def update_client(
    client_id: int = Path(...),
    client: schemas.ClientCreate = Body(...),
    db: Session = Depends(get_db)
):
    '''
    Update a Client.

    This path operation create a client in the app.

    Parameters:
    * Reqguest path and body parameter.
        * client_id: int
        * client: client

    Returns a json with the basic client information.
    * id: UUID.
    * name: str.
    * is_active: boolean.
    * loans: list[loans]
    '''
    return utils.update_client(db=db, client_id=client_id, client=client)


@router.delete(
    path="/clients/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Clients"]
)
def delete_client(
    client_id: int = Path(...),
    db: Session = Depends(get_db)
):
    '''
    delete a Client.

    This path operation Delete a client in the app.
    '''
    flag = utils.delete_client(db=db, client_id=client_id)

    if not flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"this client {client_id}, not Exists!."
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
