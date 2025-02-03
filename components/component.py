from typing import TYPE_CHECKING, List
from collections.abc import Callable
if TYPE_CHECKING:
    from game_objects import *

class Component:

    def __init__(self):
        self.owner: GameObject = None
        self._methods = {}  # Dictionary to store dynamically registered methods

    def add_method(self, names: List[str], func: Callable):
        """Register a method for this component."""
        for name in names:
            self._methods[name] = func

    def attach_to(self, owner):
        self.owner = owner

    def get_methods(self):
        return self._methods
    
    def key(self) -> str:
        return self.__class__.__name__.lower()
    
    def try_call(self, function_name):
        function = getattr(self, function_name, None)
        if callable(function):
            function()
