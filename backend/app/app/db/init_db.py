import logging
import csv

from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_employee_code(db, employee_code=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                company_code=settings.COMPANY_CODE,
                employee_code=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PW,
                is_superuser=True,
                is_active=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. UserResponse with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
        
    if settings.INITIAL_DATA_PATH:
        with open(settings.INITIAL_DATA_PATH, newline='') as fp:
            csv_reader = csv.DictReader(f=fp, delimiter=',')
            for row in csv_reader:
                user_in = schemas.UserCreate(
                    company_code=settings.COMPANY_CODE,
                    employee_code=row['employee_code'],
                    password=row['password'],
                    is_superuser=False,
                    is_active=True,
                )
                _ = crud.user.create(db, obj_in=user_in)