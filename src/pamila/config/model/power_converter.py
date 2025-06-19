from typing import Hashable

from pydantic import BaseModel


class ResponseModel(BaseModel):
    settle_time: float  # seconds
    timeout: float  # seconds


class PowerConverterInterface(BaseModel):
    setpoint: str  # e.g., 'CHANNEL:QF1C01A:SP'
    readback: str  # e.g., 'CHANNEL:QF1C01A:RB'


class PowerConverter(BaseModel):
    id: Hashable
    interface: PowerConverterInterface
    response: ResponseModel
