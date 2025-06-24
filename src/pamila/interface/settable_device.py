from abc import ABCMeta, abstractmethod


class SettableDevice(metaclass=ABCMeta):
    @abstractmethod
    def set_value(self, v):
        pass

    def get_value(self):

    def get_state(self):
        """
        Todo:
            use your internal channels to find out if you
            are ok or not
        """


class BESsyiiPowerConverter(SettableDevice):
    def get_value(self):
        """return the setpoint

        Should one check the state?
        """

    def get_state(self):
        """compare that readback is within range of setpoing

        """


class ADCRegualtedPowerConverter>

