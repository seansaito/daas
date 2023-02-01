import typing as t

from pydantic import BaseModel

class UserBase(BaseModel):
    company_code: t.Optional[str]
    employee_code: t.Optional[str]
    password: t.Optional[str]
    is_superuser: bool = False

class UserCreate(UserBase):
    ...

class UserUpdate(UserBase):
    ...

class UserInDBBase(UserBase):
    id: t.Optional[int] = None
    
    class Config:
        orm_mode = True
    

class User(UserInDBBase):
    ...
