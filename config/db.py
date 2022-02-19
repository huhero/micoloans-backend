# Python
import os

# SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE CREDENTIALS
USER = os.environ["MICO_DB_USER"]
PASSWORD = os.environ["MICO_DB_PASSWORD"]
HOST = os.environ["MICO_DB_HOST"]
PORT = os.environ["MICO_DB_PORT"]
DATABASE = os.environ["MICO_DB_DATABASE"]

SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    USER, PASSWORD, HOST, PORT, DATABASE)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
