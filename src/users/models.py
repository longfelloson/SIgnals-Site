from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
)

from database import Base


class User(Base):
    __tablename__ = "users"

    id_ = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
