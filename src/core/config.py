from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import cloudinary


class AppSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    db_url: str = Field(alias="DB_URL")

    jwt_secret: SecretStr = Field(
        alias="JWT_SECRET"
    )

    jwt_algorithm: str = Field(
        alias="JWT_ALGORITHM"
    )

    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    smtp_email: str
    smtp_password: str
    smtp_host: str
    smtp_port: int
    
    cloudinary_cloud_name: str = Field(
        alias="CLOUDINARY_CLOUD_NAME"
    )

    cloudinary_api_key: str = Field(
        alias="CLOUDINARY_API_KEY"
    )

    cloudinary_api_secret: str = Field(
        alias="CLOUDINARY_API_SECRET"
    )
settings = AppSettings()

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)