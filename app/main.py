import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import *
import asyncio
from app.db.session import create_tables

app = FastAPI()

app.include_router(auth_router)
app.include_router(cities_router)
app.include_router(users_router)
app.include_router(events_router)
app.include_router(weather_router)

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")


class AuthRedirectException(Exception):
    pass

@app.exception_handler(AuthRedirectException)
async def auth_redirect_handler(request: Request, exc: AuthRedirectException):
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)