from datetime import timedelta, datetime

from fastapi import (
    Request,
    HTTPException,
    status,
)
from jose import jwt

from auth.schemas import AccessToken
from config import settings


def create_access_token(username: str) -> AccessToken:
    data = {
        "exp": datetime.now() + timedelta(minutes=60),
        "username": username,
    }
    token = AccessToken(
        access_token=jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM),
        token_type_="Access Token"
    )
    return token


def get_token_payload(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def verify_access_token(request: Request):
    """Extract JWT token from request if token is valid otherwise raise exception."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    try:
        payload = get_token_payload(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
