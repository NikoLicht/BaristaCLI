from typing import TYPE_CHECKING, List, Dict
from collections.abc import Callable
from src.action_object import ActionObject
if TYPE_CHECKING:
    from game_objects import *

class Component:

    def __init__(self):
        self.owner: GameObject = None
        self._methods = {}  # Dictionary to store dynamically registered methods
        self.methodQueue: Dict[ActionObject, Callable] = {}

    def add_method(self, action_object: ActionObject, func: Callable):
        if self.owner:
            self.owner.register_callable_method(action_object, func)
        else:
            self.methodQueue[action_object] = func

    def attach_to(self, owner):
        self.owner = owner
        if self.owner:
            for action_object, func in self.methodQueue.items():
                self.owner.register_callable_method(action_object, func)
            self.methodQueue.clear()


    def get_methods(self):
        return self._methods
    
    def key(self) -> str:
        return self.__class__.__name__.lower()
    
    def try_call(self, function_name):
        function = getattr(self, function_name, None)
        if callable(function):
            function()
