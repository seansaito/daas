import typing as t

from pydantic import BaseModel

class UserBase(BaseModel):
    company_code: t.Optional[str]
    employee_code: t.Optional[str]
    password: t.Optional[str]
    is_superuser: bool = False
    is_active: bool = True
    work_start: t.Optional[int]
    work_end: t.Optional[int]
    rest_start: t.Optional[int]
    rest_end: t.Optional[int]

class UserCreate(UserBase):
    ...

class UserUpdate(UserBase):
    ...

class UserUpdateTime(BaseModel):
    work_start: t.Optional[int]
    work_end: t.Optional[int]
    rest_start: t.Optional[int]
    rest_end: t.Optional[int]

class UserInDBBase(UserBase):
    id: t.Optional[int] = None
    
    class Config:
        orm_mode = True
    

class UserResponse(UserInDBBase):
    ...

class UserSearchResults(BaseModel):
    results: t.Sequence[UserResponse]
    