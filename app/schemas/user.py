import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    created_at: datetime.datetime

    class Config:
        orm_mode = True
