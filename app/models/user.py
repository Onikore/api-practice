import datetime

from sqlalchemy import Integer, Column, String, DateTime

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
