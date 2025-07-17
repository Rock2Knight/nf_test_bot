from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    TOKEN: str
    ADMINS: str
    
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8"
    )

    def get_db_url(self):
        return self.DATABASE_URL


    def get_token(self):
        return self.TOKEN

    def get_admins(self):
        return self.ADMINS
        
settings = Settings()