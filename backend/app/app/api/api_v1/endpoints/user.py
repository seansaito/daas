from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.user import UserSearchResults, UserUpdate, UserResponse, UserUpdateTime

router = APIRouter()


@router.get("/", status_code=200, response_model=UserSearchResults)
def get_all_users(
        db: Session = Depends(deps.get_db),
        current_super_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Get all users (for admins only)"""
    list_users = crud.user.get_all(db=db)
    
    return {"results": list_users}


@router.get("/me", status_code=200, response_model=UserResponse)
def get_user(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
) -> UserResponse:
    """Get details of user  """
    return current_user


@router.post("/", status_code=201, response_model=UserResponse)
def update_active_status(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> UserResponse:
    """Update the active status for the user"""
    if not current_user:
        raise HTTPException(
            status_code=400, detail="User not found"
        )
    
    user_in = UserUpdate(**current_user.__dict__)
    user_in.is_active = not current_user.is_active
    updated_user = crud.user.update(
        db=db, db_obj=current_user, obj_in=user_in
    )
    
    return updated_user


@router.post("/timing", status_code=201, response_model=UserResponse)
def update_timings(
        *,
        user_in: UserUpdateTime,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> UserResponse:
    """
    Update the timings for dakoku. Integers must be between 0-23 (anything beyond this will be taken with a mod)
    """
    if not current_user:
        raise HTTPException(
            status_code=400, detail="User not found"
        )
    dict_user_in = user_in.dict()
    user_to_update = UserUpdate(**current_user.__dict__)
    for key in ["work_start", "work_end", "rest_start", "rest_end"]:
        if dict_user_in[key]:
            val = int(dict_user_in[key]) % 24
            user_to_update.__setattr__(key, val)

    updated_user = crud.user.update(
        db=db, db_obj=current_user, obj_in=user_to_update
    )
    return updated_user
