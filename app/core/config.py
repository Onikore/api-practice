import os

from dotenv import load_dotenv
from pydantic import BaseSettings

# dotenv_path = Path().cwd().parent / '.env'
load_dotenv()


class Settings(BaseSettings):
    # POSTGRES CREDS
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: int = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_URL: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # TOKEN CONST
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"

    # URLS
    ITEMS_URL: str = os.getenv('ITEMS_URL')

    # SQL QUERIES
    SELECT_SQL: str = os.getenv('SELECT_SQL')
    INSERT_SQL: str = os.getenv('INSERT_SQL')
    UPDATE_SQL: str = os.getenv('UPDATE_SQL')

    class Config:
        case_sensitive = True


settings = Settings()
