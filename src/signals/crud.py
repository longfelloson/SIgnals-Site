from typing import Optional, List, Union

from sqlalchemy import (
    insert,
    delete,
    select,
    Column, update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from signals.enums import SignalType
from signals.models import Signal
from signals.schemas import CreateSignal
from users.models import User


async def create_signal(user_id: int, signal: CreateSignal, session: AsyncSession) -> None:
    await session.execute(insert(Signal).values(user_id=user_id, **signal.model_dump()))
    await session.commit()


async def get_signals_by_username(
    username: str,
    session: AsyncSession,
    limit: int = None,
) -> List[Optional[Signal]]:
    signals = await session.execute(select(Signal).limit(limit).join(User).where(User.username == username))
    return signals.scalars().all()


async def get_signals_by_user_id(user_id: int, session: AsyncSession) -> List[Optional[Signal]]:
    signals = await session.execute(select(Signal).where(Signal.user_id == user_id))
    return signals.scalars().all()


async def update_signals(
    user_id: int,
    session: AsyncSession,
    **values
) -> None:
    """Update user's signals by user's ID"""
    await session.execute(update(Signal).where(Signal.user_id == user_id).values(**values))
    await session.commit()


async def delete_signals(
    user_id: int,
    session: AsyncSession,
    type_: SignalType = None,
) -> None:
    """Delete user's signals by provided options"""
    stmt = delete(Signal).where(Signal.user_id == user_id)
    if type_:
        stmt = stmt.and_(Signal.type_ == type_)

    await session.execute(stmt)
    await session.commit()


async def get_last_signal_by_username(
    username: str,
    session: AsyncSession,
    type_: SignalType = None,
) -> Optional[Signal]:
    """Get last user signal by username"""
    stmt = select(Signal).join(User).where(User.username == username)
    if type_:
        stmt = stmt.and_(Signal.type_ == type_)

    signal = await session.execute(stmt.order_by(Signal.created_at).limit(1))
    return signal.scalar_one_or_none()
