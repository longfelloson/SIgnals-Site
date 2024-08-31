from typing import Annotated

from fastapi import Request, Depends

from auth.schemas import AccessToken
from auth.token import verify_access_token

from database import AsyncSession
from users import crud
from users.models import User


async def get_current_user(request: Request, session: AsyncSession) -> User:
    """Gets current user from cookies by JWT-token"""
    payload = verify_access_token(request)
    user = await crud.get_user_by_username(payload["username"], session)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

