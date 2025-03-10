from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from ..db import *
from ..core import *
import jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Bearer ")

templates = Jinja2Templates(directory="./Templates")
router.mount("/Static", StaticFiles(directory="./Static"), name="static")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=168)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta #now date + 7 days (168 hours)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload  #useful load mail + exp(time)
    except jwt.ExpiredSignatureError: #token has expired
        return None
    except jwt.PyJWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

# @router.post("/token", response_model=Token)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user_id: int = Depends(get_current_user)):

    username = "Sign In"
    city = "City"

    try:
        username = UserCRUD.get_user(user_id)
        city =  UserCRUD.get_city(user_id)

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "button_text": username,
            "city": city,
        },
    )

@router.get("/login")
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/registration")
async def read_registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})