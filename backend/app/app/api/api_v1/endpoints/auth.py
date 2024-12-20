from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import schemas
from app import crud
from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token,
)
from app.models.user import User

router = APIRouter()


@router.post('/login')
def login(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Get the JWT for a user with data from OAuth2 request form body"""
    user = authenticate(employee_code=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer"
    }


@router.get('/me', response_model=schemas.UserResponse)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current user
    """
    user = current_user
    return user.__dict__

@router.post("/signup", response_model=schemas.UserResponse, status_code=201)
def create_user_signup(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.user.UserCreate,
        current_super_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """Create new user without the need to be logged in"""
    user = db.query(User).filter(User.employee_code == user_in.employee_code).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user

