# game_objects/__init__.py
from .game_object import GameObject
from .aeropress import AeroPress
from .water import Water
from .beans import Beans
from .grinder import Grinder
from .mixture import Mixture
from .kettle import Kettle
from .ketchup import Ketchup
from .puck import Puck
from .fridge import Fridge

# Define the public API of the package
__all__ = ["GameObject", "AeroPress", "Water", "Beans", "Grinder", "Mixture", "Kettle", "Ketchup", "Puck", "Fridge"]


