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


    def get_current(self):
        return 0.0


class PowerConverterDevice:
    def __init__(self, pc_model : PowerConverter):
        self.model = pc_model
        self.setpoint = epics.PV(self.model.interface.setpoint)
        self.readback = epics.PV(self.model.interface.readback)

    def get_current(self):
        return self.setpoint.get()



class PowerConverterDevice:
    """
    use update pattern ....
    """
    def __init__(self, pc_model: PowerConverter, msg_bus):
        self.model = pc_model
        self.msg_bus = msg_bus

    def set_current(self, value):
        self.msg_bus.update(dev_id=self.model.id, prop_id="set_current", value=value)
        pass

    def get_current(self):
        return
        return self.setpoint.get()


