from operator import and_, or_
from typing import Optional, Union

from pydantic import EmailStr
from sqlalchemy import (
    select,
    insert,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import (
    CreateUser,
    UserCredentials,
)
from users.models import User
from users.schemas import UpdateBalance


async def create_user(user: CreateUser, session: AsyncSession) -> None:
    await session.execute(insert(User).values(**user.model_dump()))
    await session.commit()


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.id_ == user_id))
    return user.scalar_one_or_none()


async def get_user_by_username(username: str, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.username == username))
    return user.scalar_one_or_none()


async def get_user_by_email(email: EmailStr, session: AsyncSession) -> Optional[User]:
    user = await session.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()


async def get_user_by_options(session, **options) -> Optional[User]:
    """Get user by provided options"""
    if not options:
        raise ValueError("Options have to filled")

    user = await session.execute(select(User).filter_by(**options))
    return user.scalar_one_or_none()


async def get_user_by_username_and_email(
    email: EmailStr,
    username: str,
    session: AsyncSession
) -> Optional[User]:
    user = await session.execute(select(User).where(or_(User.username == username, User.email == email)))
    return user.scalar_one_or_none()


async def update_user_balance(
    user_id: int,
    data: UpdateBalance,
    session: AsyncSession,
) -> None:
    """If amount > 0 increase user's balance otherwise decrease user's balance.'"""
    stmt = (
        update(User)
        .where(User.id_ == user_id)
        .values(balance=User.balance + data.amount if data.amount > 0 else User.balance - abs(data.amount))
    )
    await session.execute(stmt)
    await session.commit()


async def get_user_balance(user_id: int, session: AsyncSession) -> Union[int, float]:
    user_balance = await session.execute(select(User.balance).where(User.id_ == user_id))
    return user_balance.scalar_one()
