import logging
from pathlib import Path
from typing import Mapping, Sequence, Dict

from pamila.managers.model.elementmodel import MagnetElementSetup
from .model.identifiers import LatticeElementPropertyID, DevicePropertyID, ConversionID
from .model.liaison_manager import LiaisonManager
from .model.translator_service import TranslatorService
from ..config.model.magnet import EnergyDependentConversion
from ..config.service import ConfigService

logger = logging.getLogger("pamila")

from ..config.repository.querries import get_magnets
def build_managers_from_config(config_dir: Path) -> (LiaisonManager, TranslatorService):
    # Load data from YAML config files
    # service = ConfigService(
    #     magnet_path=config_dir / "magnets.yaml",
    #     pc_path=config_dir / "power_converters.yaml"
    # )
    # service.load()
    magnets = magnet_infos_from_db()

    # --- Build inverse LUT ---
    # inverse_lut: Mapping[DevicePropertyID, list[LatticeElementPropertyID]] = {
    #     DevicePropertyID(device_name=m.power_converter_id, property="set_current"): [
    #         LatticeElementPropertyID(element_name=m.elem_id, property="main_strength")
    #     ]
    #     for m in magnets
    # }
    inverse_lut: Mapping[DevicePropertyID, list[LatticeElementPropertyID]] = {
        # DevicePropertyID(device_name=m.pc, property="set_current"): [
        #     LatticeElementPropertyID(element_name=m.elem_id, property="main_strength")
        # ]
        DevicePropertyID(device_name=m.pc, property="set_current"): [
            LatticeElementPropertyID(element_name=m.name, property="main_strength")
        ]
        for m in magnets
    }

    # --- Build translator LUT ---
    translator_lut: Mapping[ConversionID, EnergyDependentConversion] = {
        ConversionID(
            # lattice_property_id=LatticeElementPropertyID(
            #     element_name=m.elem_id,
            #     property="main_strength"
            # ),
            lattice_property_id=LatticeElementPropertyID(
                element_name=m.name,
                property="main_strength"
            ),
            # ice_property_id=DevicePropertyID(
            #     device_name=m.power_converter_id,
            #     property="set_current"
            # )
            device_property_id=DevicePropertyID(
                device_name=m.pc,
                property="set_current"
            )
        ): EnergyDependentConversion(
            # todo: find out if it is the correct converion
            #  magnetic strength is most proably None
            slope=None or 1.0 / m.magnetic_strength,
            intercept=0.0,
            conversion_type="linear",
        )
        for m in magnets
    }

    # Optional: build forward LUT if needed
    forward_lut = None

    lm = LiaisonManager(forward_lut=forward_lut, inverse_lut=inverse_lut)
    tm = TranslatorService(translator_lut)

    return lm, tm
def magnet_infos_from_db() -> Sequence[MagnetElementSetup]:
    return [MagnetElementSetup(**remove_id(info)) for info in get_magnets().to_list()]

def remove_id(d: Dict) -> Dict:
    nd = d.copy()
    del d
    del nd["_id"]
    return nd


# Example usage
if __name__ == "__main__":
    import pprint

    lm, tm = build_managers_from_config(Path("config"))
    dev_prop_id = DevicePropertyID(device_name="Q3P1T6R", property="set_current")
    r, = lm.inverse(dev_prop_id)
    to = tm.get(ConversionID(lattice_property_id=r, device_property_id=dev_prop_id))
    pprint.pprint(to)
