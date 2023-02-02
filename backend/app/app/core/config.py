from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import List, Optional, Union

from app import DATA_DIR


class Settings(BaseSettings):  # 1
    API_V1_STR: str = "/api/v1"  # 2
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:8001",  # type: ignore
    ]
    
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[
        str
    ] = "https.*\.(netlify.app|herokuapp.com)"  # noqa: W605
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)  # 3
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgres://"
    FIRST_SUPERUSER: str = "150127"
    FIRST_SUPERUSER_PW: str = "dakokuai"
    COMPANY_CODE: str = "Bcg237"
    
    INITIAL_DATA_PATH: str = str(DATA_DIR / 'accounts.csv')
    
    class Config:
        case_sensitive = True  # 4


settings = Settings()  # 5