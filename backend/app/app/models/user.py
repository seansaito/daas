from sqlalchemy import Integer, String, Column, Boolean

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    company_code = Column(String(256), nullable=False)
    employee_code = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    work_start = Column(Integer, nullable=False, default=9)
    work_end = Column(Integer, nullable=False, default=20)
    rest_start = Column(Integer, nullable=False, default=12)
    rest_end = Column(Integer, nullable=False, default=13)
    