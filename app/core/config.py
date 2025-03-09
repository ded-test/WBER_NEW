from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")

SECRET_KEY = os.getenv("SECRET_KEY")

class UserSettings(BaseModel):
    SECRET_KEY: str = SECRET_KEY
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    API_KEY_WEATHER: str = API_KEY_WEATHER
