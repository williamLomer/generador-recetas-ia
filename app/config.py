from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Generador de Recetas con IA"
    database_url: str = "sqlite:///./recetas.db"
    secret_key: str = "development-only-change-this-secret-key"
    access_token_expire_minutes: int = 60
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_site_url: str = "http://localhost:8000"
    openrouter_app_name: str = "Generador de Recetas"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
