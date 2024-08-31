from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Request,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from auth.password import check_password, hash_password
from auth.schemas import (
    RegisterUser,
    CreateUser,
    UserLoginCredentials,
    AccessToken,
)
from auth.token import create_access_token
from config import settings
from database import AsyncSession
from users import crud

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)


@router.get("/register", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def create_user(session: AsyncSession, data: RegisterUser):
    """User registration process"""
    user = await crud.get_user_by_username_and_email(data.email, data.username, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": "User already exists"},
        )

    credentials = CreateUser(**data.model_dump(), hashed_password=hash_password(data.password))
    await crud.create_user(credentials, session)

    token = create_access_token(data.email)
    return JSONResponse({"msg": "User created successfully", "access_token": token.access_token})


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=AccessToken, status_code=status.HTTP_201_CREATED)
async def login_user(
    session: AsyncSession,
    credentials: UserLoginCredentials,
):
    user = await crud.get_user_by_email(credentials.email, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Invalid credentials or user doesn't exist"},
        )

    if not check_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Invalid password"},
        )

    access_token = create_access_token(user.username)
    return access_token


@router.post('/logout', response_class=JSONResponse)
async def logout_user():
    """Return response without user's access token in cookies"""
    response = JSONResponse(content={"msg": "User successfully logged out"})
    response.delete_cookie("access_token")

    return response
