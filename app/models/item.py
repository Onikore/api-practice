from sqlalchemy import Column, String, Float, BigInteger

from app.db.base_class import Base


class Item(Base):
    id = Column(BigInteger, primary_key=True,autoincrement=False, unique=True, nullable=False)
    image_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
