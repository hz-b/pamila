# from pamila.config.interface.accelerator_lattice import AcceleratorLattice
# instantiate lattice and calculate the quadrupole response
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import epics
from pamila.interface.settable_device import BESSYIIPowerConverter, SettableDevice

from config.bessy2_sr_reflat import bessy2Lattice
from pamila.config.service import ConfigService
from pamila.managers.build_managers_from_config import build_managers_from_config
from at import Quadrupole as ATQuadrupole, All as ATall
# first step: instantiate the machine
# second step: calculate the quadrupole response
# change strength up and down
# fit response to it
# Add 'src' to sys.path to import pamila
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
CONFIG_DIR = PROJECT_ROOT / "config"

# Define paths to config files
magnet_config_path = CONFIG_DIR / "magnets.yaml"  # adjust name if it's magnets.yaml
power_converter_config_path = CONFIG_DIR / "power_converters.yaml"

# Instantiate the config service
service = ConfigService(
    magnet_path=magnet_config_path,
    pc_path=power_converter_config_path
)

# Load data
service.load()

@dataclass
class Tunes:
    x: float
    y: float

@dataclass
class TuneMeasurement:
    dI : float
    tunes: Tunes




@dataclass
class QuadrupolePCResponse:
    id: str
    meas: Sequence[TuneMeasurement]


class TuneDevice:
    def __init__(self, prefix:str):
        self.x = epics.PV(f"{prefix}:x:tune")
        self.y = epics.PV(f"{prefix}:y:tune")

    def read(self) -> Tunes:
        return Tunes(x=self.x.get(), y=self.y.get())


# data to go to databases ....
tune_correction_quad_pcs_names = ('Q4PT4R', 'Q4P1T6R', 'Q3PD2R', 'Q3P1T6R', 'Q3PD1R', 'Q4PD6R', 'Q3P2T8R', 'Q3PD6R', 'Q3PD4R', 'Q3PT7R', 'Q4PD4R', 'Q4PD7R', 'Q4PD3R', 'Q3PD8R', 'Q3P1T1R', 'Q4PD2R', 'Q4P2T6R', 'Q3P2T1R', 'Q4PD1R', 'Q3PD3R', 'Q4P1T8R', 'Q4PT5R', 'Q3P1T8R', 'Q4P2T1R', 'Q4PD8R', 'Q3PT3R', 'Q3PT2R', 'Q3PT5R', 'Q4PT3R', 'Q4P2T8R', 'Q3PD7R', 'Q3PT4R', 'Q4P1T1R', 'Q4PT7R', 'Q4PT2R', 'Q3PD5R', 'Q3P2T6R', 'Q4PD5R')
tune_correction_quad_pcs = [BESSYIIPowerConverter(name=name, prefix=f"Anonym:{name}") for name in tune_correction_quad_pcs_names]

tune_dev = TuneDevice(f"Anonym:beam:twiss")
tune_dev.read()
#-------------------------------------------------------------------------
# Procedure for a machine with single poweered quadrupoles
# todo: not all quads are tune correction quads


lm, tm = build_managers_from_config("nothing at the moment")


class StatusResetter:
    def __init__(self, pc: SettableDevice):
        self.pc = pc
        assert self.pc.get_value() is not None
        self.ref_value = None

    def __enter__(self):
        self.ref_value = self.pc.get_value()
        return self.ref_value

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pc.set_value(self.ref_value)




def exec_step(tune_dev, sr, dI: float) -> TuneMeasurement:
    sr.pc.set_value( sr.ref_value + dI)
    tunes = tune_dev.read()
    return TuneMeasurement(dI=dI, tunes=tunes)


def exec_one_quad_pcs(quad, dIs: Sequence[float]):
    sr = StatusResetter(quad)
    with sr:
        tunes = [exec_step(tune_dev, sr, dI) for dI in dIs]
    r = QuadrupolePCResponse(id=quad.name, meas=tunes)
    return r


measurements = [exec_one_quad_pcs(quad, [0, -0.001, 0, 0.001, 0]) for quad in tune_correction_quad_pcs[:3]]
measurements