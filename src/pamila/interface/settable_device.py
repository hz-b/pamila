from abc import ABCMeta, abstractmethod

import epics


class SettableDevice(metaclass=ABCMeta):
    @abstractmethod
    def set_value(self, v):
        raise NotImplementedError("use derived")

    @abstractmethod
    def get_value(self):
        raise NotImplementedError("use derived")

    @abstractmethod
    def get_state(self):
        """
        Todo:
            use your internal channels to find out if you
            are ok or not
        """
        raise NotImplementedError("use derived")


class BESSYIIPowerConverter(SettableDevice):
    def __init__(self, name: str, prefix: str):
        self.name = name
        self.setpoint = epics.PV(f"{prefix}:set")
        self.readback = epics.PV(f"{prefix}:rdbk")

    def get_value(self):
        """return the setpoint

        Should one check the state?
        """
        return self.setpoint.get()

    def set_value(self, v):
        self.setpoint.put(v)

    def get_state(self):
        """compare that readback is within range of setpoing
        """
        raise NotImplementedError("don't know state yet")


