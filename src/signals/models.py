from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Float,
    DateTime,
)

from database import Base


class Signal(Base):
    __tablename__ = "signals"

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id_'))
    type_ = Column(String)
    tp = Column(Float)
    sl = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
