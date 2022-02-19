# SqlAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


# Conf DB
from config.db import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(String, unique=True, index=True)
    amount = Column(Integer)
    term = Column(Integer)
    interest_rate = Column(Float(1, 2))

    client_id = Column(Integer, ForeignKey("clients.id"))
    is_active = Column(Boolean, default=True)

    client = relationship("Client", back_populates="loans")
