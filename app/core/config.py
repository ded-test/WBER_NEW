from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

class UserSettings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    API_KEY_WEATHER: str = os.getenv("API_KEY_WEATHER")

settings = UserSettings()
