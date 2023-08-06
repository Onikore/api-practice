from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, items

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(items.router, prefix='/items', tags=['items'])
