from app.db import base
from app.db.base_class import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)
