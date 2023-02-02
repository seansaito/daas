from sqlalchemy import Integer, String, Column, Boolean

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    company_code = Column(String(256), nullable=False)
    employee_code = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    