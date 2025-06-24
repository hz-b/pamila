# from pamila.config.interface.accelerator_lattice import AcceleratorLattice
# instantiate lattice and calculate the quadrupole response
from pathlib import Path

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


# data to go to databases ....
tune_correction_quad_pcs = ('Q4PT4R', 'Q4P1T6R', 'Q3PD2R', 'Q3P1T6R', 'Q3PD1R', 'Q4PD6R', 'Q3P2T8R', 'Q3PD6R', 'Q3PD4R', 'Q3PT7R', 'Q4PD4R', 'Q4PD7R', 'Q4PD3R', 'Q3PD8R', 'Q3P1T1R', 'Q4PD2R', 'Q4P2T6R', 'Q3P2T1R', 'Q4PD1R', 'Q3PD3R', 'Q4P1T8R', 'Q4PT5R', 'Q3P1T8R', 'Q4P2T1R', 'Q4PD8R', 'Q3PT3R', 'Q3PT2R', 'Q3PT5R', 'Q4PT3R', 'Q4P2T8R', 'Q3PD7R', 'Q3PT4R', 'Q4P1T1R', 'Q4PT7R', 'Q4PT2R', 'Q3PD5R', 'Q3P2T6R', 'Q4PD5R')
#-------------------------------------------------------------------------
# Procedure for a machine with single poweered quadrupoles
# todo: not all quads are tune correction quads

ring = bessy2Lattice()
lm, tm = build_managers_from_config("nothing at the moment")

quads = [elm for elm in ring if isinstance(elm, ATQuadrupole)]
tune_correction_quads = [quad for quad in quads if quad.FamName[1] in ["3", "4"]]


class StatusResetter:
    def __init__(self, quad):
        self.quad = quad
        self.ref_value = None

    def __enter__(self):
        self.ref_value = quad.K
        return self.ref_value

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quad.K = self.ref_value

for quad in tune_correction_quads:
    sr = StatusResetter(quad)
    with sr:
        for dk in [0, 0.001, 0, -0.001, 0]:
            quad.K = sr.ref_value + dk
            tunes = ring.get_optics(ATall)[1]['tune']
    pc = service.get_power_converter(quad.power_converter_id)
    print(pc.id)

    ref_current = pc.get_current()

    # measure at dI =0 zero

    # measure at -dI, lower level
    # measure at dI=0, zero
    # measure at -dI, higher level
    # measure at dI=0, zero

# calcuate repsonse matrix
# derive correction from response matrix
# -------------------------------------------------------------------------

# how it is done for BESSY II
# quads = service.get_quadrupoles()
# need to know which power converters are the ones that were
# foressen to do tune correction
# should be Q3/Q4 ... perhaps Q5

# then apply the steps to the power converters