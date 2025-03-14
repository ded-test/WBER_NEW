from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
import bcrypt
import jwt
from ..db import *
from ..core import *

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Bearer ")

templates = Jinja2Templates(directory="./Templates")
router.mount("/Static", StaticFiles(directory="./Static"), name="static")

class AuthRedirectException(Exception):
    pass

@router.exception_handler(AuthRedirectException)
async def auth_redirect_handler(request: Request, exc: AuthRedirectException):
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


def create_access_token(user_id: int, expires_delta: timedelta = timedelta(hours=168)):
    to_encode = {"sub": str(user_id)}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload  # useful load mail + exp(time)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user_id: int = Depends(get_current_user)):
    username = "Sign In"
    city = "City"

    try:
        user = await UserCRUD.get_user(user_id)
        username = user.username
        city = user.city
    except Exception as e:
        pass

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

@router.post("/login")
async def submit_login(request: Request):
    form = await request.form()
    mail = form.get("mail")
    password = form.get("password")

    user = await UserCRUD.get_user(mail)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password):
        access_token = create_access_token(user_id=user.id)

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=86400,  # 1 day
        )
        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

@router.post("/register")
async def submit_register(request: Request):
    form = await request.form()
    username = form.get("username")
    city = form.get("city")
    mail = form.get("mail")
    password = form.get("password")

    if not all([username, city, mail, password]):
        raise HTTPException(status_code=400, detail="All fields are required")

    existing_user = await UserCRUD.check_username(username)
    if not existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = await UserCRUD.check_mail(mail)
    if not existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        await UserCRUD.create_user(
            username=username,
            city=city,
            mail=mail,
            password=hashed_password,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register user: {str(e)}"
        )

    return RedirectResponse(url="/login", status_code=303)
