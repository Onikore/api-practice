from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api import deps
from app.core import security
from app.schemas.token import Token
from app.schemas.user import UserCreate

router = APIRouter()


@router.post('/signup', response_model=Token)
def sign_up(user_data: UserCreate, db: Session = Depends(deps.get_db)):
    user = crud.user.create(db, obj_in=user_data)

    return Token(
        access_token=security.create_access_token(user.id),
        token_type="bearer"
    )


@router.post('/login', response_model=Token)
def login(db: Session = Depends(deps.get_db),
          form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")

    return Token(
        access_token=security.create_access_token(user.id),
        token_type="bearer"
    )
