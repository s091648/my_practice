from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    csv_path: Path = Path("data/backend_users.csv")
    csv_upload_path: Path = Path("data/upload")

settings = Settings()
