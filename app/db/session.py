from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

db = Database(settings.DB_URL)
engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
