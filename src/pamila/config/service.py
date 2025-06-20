from .model.magnet import MagneticObject
from .model.power_converter import PowerConverter
from .repository.file_repository import FileRepository


class ConfigService:
    def __init__(self, magnet_path: str, pc_path: str):
        self.magnet_repo = FileRepository(MagneticObject, magnet_path)
        self.pc_repo = FileRepository(PowerConverter, pc_path)
        self._magnets = None
        self._power_converters = None

    def load(self):
        self._magnets = self.magnet_repo.load()
        self._power_converters = {pc.id: pc for pc in self.pc_repo.load()}

    def get_magnets(self):
        return self._magnets

    def get_power_converter(self, id):
        return self._power_converters[id]
