# SqlAlchemy
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


# Conf DB
from config.db import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nit = Column(String, unique=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="client")
