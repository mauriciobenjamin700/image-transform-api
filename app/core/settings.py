from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = Field(
        title="URL do banco de dados",
        description="URL do banco de dados",
        default="postgresql://user:password@localhost:5432/database"
    )
    TEST_DB_URL: str = Field(
        title="URL do banco de dados de teste",
        description="URL do banco de dados de teste",
        default="sqlite:///:memory:"
    )


    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


config = Settings()
