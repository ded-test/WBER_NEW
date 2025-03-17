from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

class DBSettings(BaseModel):
    DATABASE_URL: str

    @classmethod
    def load(cls) -> "DBSettings":
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        if not DB_PORT.isdigit():
            raise ValueError(f"Invalid database port: {DB_PORT}")

        DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        return cls(DATABASE_URL=DATABASE_URL)

db_settings = DBSettings.load()
