from fastapi import APIRouter

from app.api.api_v1.endpoints import user, auth


api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["recipes"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
