from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.user import UserSearchResults

router = APIRouter()


@router.get("/users", status_code=200, response_model=UserSearchResults)
def get_all_users(
        db: Session = Depends(deps.get_db),
        current_super_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    list_users = crud.user.get_all(db=db)
    
    return {"results": list_users}
