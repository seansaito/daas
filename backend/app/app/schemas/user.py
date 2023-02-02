import typing as t

from pydantic import BaseModel

class UserBase(BaseModel):
    company_code: t.Optional[str]
    employee_code: t.Optional[str]
    password: t.Optional[str]
    is_superuser: bool = False
    is_active: bool = True

class UserCreate(UserBase):
    ...

class UserUpdate(UserBase):
    ...

class UserInDBBase(UserBase):
    id: t.Optional[int] = None
    
    class Config:
        orm_mode = True
    

class UserResponse(UserInDBBase):
    ...

class UserSearchResults(BaseModel):
    results: t.Sequence[UserResponse]
    