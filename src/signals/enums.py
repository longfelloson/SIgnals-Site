from enum import Enum


class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    PENDING_BUY = "PENDING_BUY"
    PENDING_SELL = "PENDING_SELL"
    CLOSED = "CLOSED"
