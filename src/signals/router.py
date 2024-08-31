from typing import List, Union, Optional

from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from auth.token import verify_access_token
from auth.utils import CurrentUser
from database import AsyncSession
from signals import crud
from signals.enums import SignalType
from signals.schemas import CreateSignal, Signal as SignalSchema

router = APIRouter(dependencies=[Depends(verify_access_token)], tags=["Signals"])


@router.post('/signals', response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def create_signal(
    signal: CreateSignal,
    user: CurrentUser,
    session: AsyncSession,
):
    """Create signal"""
    await crud.create_signal(user.id_, signal, session)
    await utils.send_signal(signal)

    return JSONResponse({"msg": "Signal successfully created"}, status_code=status.HTTP_201_CREATED)


@router.get('/signals', response_model=Union[SignalSchema, List[SignalSchema]])
async def get_signals(
    user: CurrentUser,
    session: AsyncSession,
):
    """Get user signal"""
    signals = await crud.get_signals_by_user_id(user.id_, session)
    if not signals:
        raise HTTPException(detail={"msg": "Signals not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return signals


@router.get('/signals/{username}', response_model=List[SignalSchema])
async def get_signals_by_username(
    username: str,
    session: AsyncSession,
    limit: str = 25,
):
    """Get signals by username"""
    signals = await crud.get_signals_by_username(username, session, limit=limit)
    if not signals:
        raise HTTPException(detail={"msg": "Signals not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return signals


@router.get('/signals/{username}/last', response_model=Union[SignalSchema, List[SignalSchema]])
async def get_last_signal_by_username(
    username: str,
    session: AsyncSession,
    type_: SignalType = None,
):
    """Get signals by username"""
    signal = await crud.get_last_signal_by_username(username, session, type_=type_)
    if not signal:
        raise HTTPException(detail={"msg": "Last signal not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return signal


@router.delete("/signals")
async def delete_signals(
    user: CurrentUser,
    session: AsyncSession,
    type_: SignalType = None,
):
    """Delete user's signals or type_ if type_ id provided"""
    await crud.delete_signals(user.id_, session, type_=type_)

    return JSONResponse({"msg": "Signals successfully deleted"})


@router.patch("/signals", response_class=JSONResponse)
async def update_signals(
    user: CurrentUser,
    session: AsyncSession,
    type_: SignalType = None,
):
    """Update user's signals"""
    await crud.update_signals(user.id_, session, type_=type_)

    return JSONResponse({"msg": "All signals successfully updated"})
