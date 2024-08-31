from typing import Union

from pydantic import BaseModel


class UpdateBalance(BaseModel):
    amount: Union[int, float]
