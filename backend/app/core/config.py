from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """
    app_name: str = "Election Assistant API"
    google_api_key: str = ""
    google_project_id: str = ""  # For Vertex AI
    google_location: str = "us-central1" # Default Vertex AI location
    environment: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
