from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    LOG_LEVEL: str = "INFO"
    API_KEY_HEADER_NAME: str = "x-api-key"
    # We can check a hardcoded key for the hackathon or specific logic
    # The requirement says "x-api-key: YOUR_SECRET_API_KEY"
    # We might want to enforce a specific key or just any key presence.
    # For now, let's allow setting it via env.
    HACKATHON_API_KEY: str = "secret-key" 

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
