from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    ngrok_auth_token: str = os.getenv("NGROK_AUTH_TOKEN", "")
    model_path: str = os.getenv("MODEL_PATH", "/content/drive/MyDrive/")
    port: int = int(os.getenv("PORT", "7000"))
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()