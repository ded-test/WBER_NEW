from pydantic import BaseModel
from ../../.env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, SECRET_KEY

class UserSettings(BaseModel):
    SECRET_KEY: str = SECRET_KEY
    DATABASE_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"