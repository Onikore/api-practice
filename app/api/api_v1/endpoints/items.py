from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.item import ItemUpdate, ItemInDB

router = APIRouter()


@router.get('/{id}', response_model=ItemInDB)
def get_item(id: int, db: Session = Depends(deps.get_db)):
    item = crud.item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found")
    return item


@router.get('/', response_model=List[ItemInDB])
def get_multi_items(skip=0, limit=5, db: Session = Depends(deps.get_db)):
    return crud.item.get_multi(db, skip=skip, limit=limit)


@router.put('/{id}', response_model=ItemInDB)
def update_item(id: int,
                obj_in: ItemUpdate,
                current_user: User = Depends(deps.get_current_user),
                db: Session = Depends(deps.get_db)):
    item = crud.item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found")
    return crud.item.update(db, db_obj=item, obj_in=obj_in)


@router.delete('/{id}', response_model=ItemInDB)
def delete_items(id: int,
                 current_user: User = Depends(deps.get_current_user),
                 db: Session = Depends(deps.get_db)):
    item = crud.item.get(db, id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found")
    return crud.item.remove(db, obj=item)
