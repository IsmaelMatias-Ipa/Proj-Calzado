from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    app_name: str = "ShoeFlow"
    ai_service_url: AnyHttpUrl = "https://example.com/ai"
    store_catalog_url: AnyHttpUrl = "https://example.com/catalog"
    stripe_api_key: str = ""
    jwt_secret_key: str = "supersecret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
