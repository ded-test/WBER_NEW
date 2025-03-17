from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

class UserSettings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    API_KEY_WEATHER: str = os.getenv("API_KEY_WEATHER", "default_api_key")

settings = UserSettings()
