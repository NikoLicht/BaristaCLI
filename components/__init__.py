# components/__init__.py
from .component import Component
from .boilable import Boilable
from .container import Container
from .drinkable import Drinkable
from .edible import Edible
from .powered import Powered
from .crankable import Crankable
from .watchable import Watchable
from .slapable import Slapable
from .trowable import Throwable

# Define the public API of the package
__all__ = ["Component", "Boilable", "Container", "Drinkable", "Edible", "Powered", "Crankable", "Watchable", "Slapable", "Throwable"]

