from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class UserSettings(BaseModel):
    DATABASE_URL: str

    @classmethod
    def load(cls) -> "UserSettings":
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return cls(DATABASE_URL=DATABASE_URL)

