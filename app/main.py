import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import *
app = FastAPI()

templates = Jinja2Templates(directory="./Templates")
app.mount("/Static", StaticFiles(directory="./Static"), name="static")

app.include_router(auth_router)
app.include_router(events_router)
app.include_router(users_router)
app.include_router(weather_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)