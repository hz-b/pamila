import sys
from pathlib import Path

# Add 'src' to sys.path to import pamila
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
CONFIG_DIR = PROJECT_ROOT / "config"

sys.path.append(str(SRC_DIR))

from src.pamila.config.service import ConfigService

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

# Use configuration
magnets = service.get_magnets()
for m in magnets:
    pc = service.get_power_converter(m.power_converter_id)
    print(f"{m.elem_id} -> PC {pc.id}, setpoint: {pc.interface.setpoint}")
