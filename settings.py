import os
from pydantic import MySQLDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_url: MySQLDsn = Field(alias="DB_URL")
    port: int = Field(alias="PORT")
    log_level: str = "INFO"
    debug: bool = True
    jwt_secret: str = Field(alias="JWT_SECRET")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_default=True,
    )

settings = Settings()
