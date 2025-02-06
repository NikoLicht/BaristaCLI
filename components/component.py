from typing import TYPE_CHECKING, List, Dict
from collections.abc import Callable
from src.action_object import ActionObject
if TYPE_CHECKING:
    from game_objects import *

class Component:

    def __init__(self):
        self.owner: GameObject = None
        self._component_methods: Dict[str, ActionObject] = {}
        self.methodQueue: List[ActionObject] = []
        self.register_required_wordQueue: List[str] = []

    def add_method(self, action_object: ActionObject):
            self._component_methods[action_object.name] = action_object
            self.register_method_game_instance(action_object)

    def attach_to(self, owner):
        self.owner = owner

        if self.owner:
            for word in self.register_required_wordQueue:
                self.owner.register_required_word(word)
            self.register_required_wordQueue.clear()

            for method in self.methodQueue:
                self.register_method_game_instance(method)

    def register_method_game_instance(self, action_object: ActionObject):
        if self.owner:
            action_object.add_game_object(self.owner)
            self.owner.game_instance.register_action(action_object)
        else:
            self.methodQueue.append(action_object)


    def register_required_word(self, word: str):
        if self.owner:
            self.owner.register_required_word(word)
        else:
            self.register_required_wordQueue.append(word)

    def get_methods(self) -> Dict[str, ActionObject]:
        return self._component_methods
    
    def key(self) -> str:
        return self.__class__.__name__.lower()
    
    def try_call(self, function_name):
        function = getattr(self, function_name, None)
        if callable(function):
            function()
