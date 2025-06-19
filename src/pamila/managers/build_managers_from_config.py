import logging
from pathlib import Path
from typing import Mapping

from .model.identifiers import LatticeElementPropertyID, DevicePropertyID, ConversionID
from .model.liaison_manager import LiaisonManager
from .model.translator_service import TranslatorService
from ..config.model.magnet import EnergyDependentConversion
from ..config.service import ConfigService

logger = logging.getLogger("pamila")


def build_managers_from_config(config_dir: Path) -> (LiaisonManager, TranslatorService):
    # Load data from YAML config files
    service = ConfigService(
        magnet_path=config_dir / "magnets.yaml",
        pc_path=config_dir / "power_converters.yaml"
    )
    service.load()
    magnets = service.get_magnets()

    # --- Build inverse LUT ---
    inverse_lut: Mapping[DevicePropertyID, list[LatticeElementPropertyID]] = {
        DevicePropertyID(device_name=m.power_converter_id, property="set_current"): [
            LatticeElementPropertyID(element_name=m.elem_id, property="main_strength")
        ]
        for m in magnets
    }

    # --- Build translator LUT ---
    translator_lut: Mapping[ConversionID, EnergyDependentConversion] = {
        ConversionID(
            lattice_property_id=LatticeElementPropertyID(
                element_name=m.elem_id,
                property="main_strength"
            ),
            device_property_id=DevicePropertyID(
                device_name=m.power_converter_id,
                property="set_current"
            )
        ): EnergyDependentConversion(
            slope=1.0 / m.conversion.slope,
            intercept=0.0,
            conversion_type=m.conversion.conversion_type,
        )
        for m in magnets
    }

    # Optional: build forward LUT if needed
    forward_lut = None

    lm = LiaisonManager(forward_lut=forward_lut, inverse_lut=inverse_lut)
    tm = TranslatorService(translator_lut)

    return lm, tm


# Example usage
if __name__ == "__main__":
    import pprint

    lm, tm = build_managers_from_config(Path("config"))
    pprint.pprint(lm.inverse(DevicePropertyID(device_name="PC_QF1C01A", property="set_current")))
