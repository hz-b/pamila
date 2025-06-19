import logging
from abc import ABCMeta, abstractmethod
from typing import Sequence, Mapping

from .identifiers import LatticeElementPropertyID, DevicePropertyID

logger = logging.getLogger("pamila")


class LiaisonManagerBase(metaclass=ABCMeta):
    """transforms pairs of (id, property)

    Warning:
        it returns a sequence of device / properties
        More than one device can be necessary to be updated

    Todo:
        review if it violates single responsibility principle?
        Should fanout and Liaison be managed separately?
    """

    @abstractmethod
    def forward(self, id_: LatticeElementPropertyID) -> Sequence[DevicePropertyID]:
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def inverse(self, id_: DevicePropertyID) -> Sequence[LatticeElementPropertyID]:
        raise NotImplementedError("use derived class instead")


class LiaisonManager(LiaisonManagerBase):
    def __init__(
            self,
            forward_lut: Mapping[LatticeElementPropertyID, Sequence[DevicePropertyID]],
            inverse_lut: Mapping[DevicePropertyID, Sequence[LatticeElementPropertyID]],
    ):
        self.forward_lut = forward_lut
        self.inverse_lut = inverse_lut

    def forward(self, id_: LatticeElementPropertyID) -> Sequence[DevicePropertyID]:
        return self.forward_lut[id_]

    def inverse(self, id_: DevicePropertyID) -> Sequence[LatticeElementPropertyID]:
        try:
            return self.inverse_lut[id_]
        except KeyError as ke:
            logger.error(
                f"{self.__class__.__name__} I did not find id {id_} in lookup table: {ke}"
            )
