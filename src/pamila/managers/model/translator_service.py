import logging
from abc import ABCMeta, abstractmethod
from typing import Mapping

from .identifiers import ConversionID

from .state_conversion import StateConversion

logger = logging.getLogger("pamila")

class TranslatorServiceBase(metaclass=ABCMeta):
    """

    Actor says:
    * I know:

         * I want to change property "A" of lattice element "B"
         * I know that device "C" needs to change property "D"

    * please give me the translation object that converts between these
    """
    @abstractmethod
    def get(self, id_: ConversionID) -> StateConversion:
        pass


class TranslatorService(TranslatorServiceBase):
    def __init__(self, lut: Mapping[ConversionID, StateConversion]):
        self.lut = lut

    def get(self, id_: ConversionID) -> StateConversion:
        try:
            return self.lut[id_]
        except KeyError as ke:
            logger.error(
                f"{self.__class__.__name__}: I did not find id {id_} in lookup table: {ke}"
            )
            od = self.objects_for_device(id_)
            logger.warning(f"{self.__class__.__name__}: For the device I know {od}")
            em = self.objects_for_lat_elem(id_)
            logger.warning(
                f"{self.__class__.__name__}: For the lattice element I know {em}"
            )
            raise ke

    def objects_for_lat_elem(self, id_: ConversionID):
        return {
            key: to
            for key, to in self.lut.items()
            if id_.lattice_property_id.element_name
               == key.lattice_property_id.element_name
        }

    def objects_for_device(self, id_: ConversionID):
        return {
            key: to
            for key, to in self.lut.items()
            if id_.device_property_id.device_name == key.device_property_id.device_name
        }

