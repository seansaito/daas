from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    
    def get_by_employee_code(self, db: Session, *, employee_code: str) -> Optional[User]:
        return db.query(User).filter(User.employee_code == employee_code).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a User and add to the db"""
        create_data = obj_in.dict()
        db_obj = User(**create_data)
        db.add(db_obj)
        db.commit()
        return db_obj


user = CRUDUser(User)
