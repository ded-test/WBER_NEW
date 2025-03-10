from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")

SECRET_KEY = os.getenv("SECRET_KEY")

class UserSettings(BaseModel):
    SECRET_KEY: str = SECRET_KEY
    API_KEY_WEATHER: str = API_KEY_WEATHER
