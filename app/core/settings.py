from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = Field(
        title="URL do banco de dados",
        description="URL do banco de dados",
        default="sqlite:///image-transform.db"
    )
    TEST_DB_URL: str = Field(
        title="URL do banco de dados de teste",
        description="URL do banco de dados de teste",
        default="sqlite:///:memory:"
    )
    UPLOAD_FOLDER: str = Field(
        title="Pasta de uploads",
        description="Pasta onde os arquivos serão salvos",
        default="uploads"
    )
    ALLOWED_EXTENSIONS: set = Field(
        title="Extensões permitidas",
        description="Extensões permitidas para upload",
        default={"png", "jpg", "jpeg", "gif"}
    )


    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


config = Settings()
