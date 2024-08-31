from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    validator,
    Field,
)

from signals.enums import SignalType


class CreateSignal(BaseModel):
    type_: SignalType
    tp: float
    sl: float
    price: Optional[float] = Field(default=None)

    @validator('price', always=True)
    def validate_price(cls, v, values):
        if values['type_'] in [SignalType.PENDING_BUY, SignalType.PENDING_SELL] and v is None:
            raise ValueError('Price is required for PENDING_BUY and PENDING_SELL signals')
        return v


class Signal(BaseModel):
    id_: int
    user_id: int
    type_: Optional[SignalType]
    tp: float
    sl: float
    price: Optional[float]
    created_at: datetime
