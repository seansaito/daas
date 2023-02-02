from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.user import UserSearchResults, UserUpdate, UserResponse

router = APIRouter()


@router.get("/users", status_code=200, response_model=UserSearchResults)
def get_all_users(
        db: Session = Depends(deps.get_db),
        current_super_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    list_users = crud.user.get_all(db=db)
    
    return {"results": list_users}

@router.post("/users", status_code=201, response_model=UserResponse)
def update_active_status(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> UserResponse:
    """Update the active status for the user"""
    if not current_user:
        raise HTTPException(
            status_code=400, detail="UserResponse not found"
        )
    
    user_in = UserUpdate(**current_user.__dict__)
    user_in.is_active = not current_user.is_active
    updated_user = crud.user.update(
        db=db, db_obj=current_user, obj_in=user_in
    )
    
    return updated_user
    