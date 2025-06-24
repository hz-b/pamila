from dataclasses import dataclass
from typing import Sequence

from at import Quadrupole as ATQuadrupole, All as ATall

from config.bessy2_sr_reflat import bessy2Lattice


class StatusResetter:
    def __init__(self, quad):
        self.quad = quad
        self.ref_value = None

    def __enter__(self):
        self.ref_value = self.quad.K
        return self.ref_value

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quad.K = self.ref_value


ring = bessy2Lattice()

quads = [elm for elm in ring if isinstance(elm, ATQuadrupole)]
tune_correction_quads = [quad for quad in quads if quad.FamName[1] in ["3", "4"]]


@dataclass
class Tunes:
    x: float
    y: float

@dataclass
class TuneMeasurement:
    dK : float
    tunes: Tunes


@dataclass
class QuadrupoleResponse:
    id: str
    meas: TuneMeasurement


def exec_step(sr, dK: float) -> TuneMeasurement:
    sr.quad.K = sr.ref_value + dK
    stat, summary, twiss =  ring.get_optics(ATall)
    tunes = summary['tune']
    return TuneMeasurement(
        dK=dK,
        tunes=Tunes(x=tunes[0],y=tunes[1])
    )


def exec_one_quad(quad, dKs: Sequence[float]):
    sr = StatusResetter(quad)
    with sr:
        tunes = [exec_step(sr, dk) for dk in dKs]
    return QuadrupoleResponse(id=quad.FamName, meas=tunes)


measurements = [exec_one_quad(quad, [-0.001, 0.001]) for quad in tune_correction_quads[:3]]
measurements