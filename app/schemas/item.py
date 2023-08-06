from pydantic import BaseModel


class ItemBase(BaseModel):
    id: int = None
    image_url: str = None
    name: str = None
    price: float = None


class ItemCreate(ItemBase):
    id: int
    image_url: str
    name: str
    price: float


class ItemUpdate(ItemBase):
    pass


class ItemInDB(ItemBase):
    id: int
    image_url: str
    name: str
    price: float

    class Config:
        orm_mode = True
