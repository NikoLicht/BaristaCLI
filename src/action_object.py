from __future__ import annotations
from .printing import *
from .grammar import *
from collections.abc import Callable
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game_objects.game_object import GameObject

class ActionObject:
    def __init__(self, name: str, required_parameter: str, allows_list: bool = False, methods: List[Callable] = [], objects: List[GameObject] = []):
        self.name = name.lower()
        self.required_parameter = None if required_parameter == "None" else required_parameter
        self.allows_list = allows_list
        self._methods = methods if methods is not None else []
        self._game_objects: List[GameObject] = objects if objects is not None else []

    def __eq__(self, other):
        return isinstance(other, ActionObject) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        gr = Grammar()
        print_str =  f"name: \"{self.name}\" - req_param: {self.required_parameter} - allow_ls: {self.allows_list}"
        if self._methods:
            print_str += "\n    Methods bound to key: " +  gr.make_list([method.__name__ + "()" for method in self._methods], "and", action)
        if self._game_objects:
            print_str += "\n    Objects implementing action: " + gr.make_list([obj.name for obj in self._game_objects])
        print_str += "\n" 

        return print_str
    
    def get_method(self):
        if not self._methods:
            return None
        return self._methods[0]
    
    def add_method(self, method: Callable):
        if(self._methods is None):
            self._methods = []
        if(method not in self._methods):
            self._methods.append(method)

    def add_action_object(self, action_object: ActionObject):
        if action_object == self:
            return  # Prevent adding itself

        if action_object.get_all_methods():
            for method in action_object.get_all_methods():
                if method not in self._methods:
                    self._methods.append(method)
        
        if action_object.get_all_game_objects():
            for game_object in action_object.get_all_game_objects():
                if game_object not in self._game_objects:
                    self._game_objects.append(game_object)

    def get_all_methods(self):
        if self._methods is None:
            return None
        return self._methods

    def add_game_object(self, game_object: GameObject):
        if self._game_objects is None:
            self.game_objects = []
        if game_object not in self._game_objects:
            self._game_objects.append(game_object)
        
    def get_game_object(self):
        if not self._game_objects:
            return None 
        return self._game_objects[0]

    def get_all_game_objects(self):
        if self._game_objects is None:
            return None
        return self._game_objects

    def help(self):
        req_param: bool = self.required_parameter is not None
        multi: bool = self.allows_list
        explanation = f"   With this action, you can {action(self.name)} a single object{"" if not multi else f" or multiple objects"}{"" if not req_param else f" {req(self.required_parameter)} a target object"}"
        explanation += "."

        primary_object = "water" if len(self._game_objects) == 0 else self._game_objects[0].name
        secondary_object = "beans" if len(self._game_objects) == 0 else self._game_objects[0].name
        tertiary_object = "beans" if len(self._game_objects) == 0 else self._game_objects[0].name
        target_object = "grinder"

        say(f"   [u]{action(self.name)} help             [/u]")
        say(explanation)
        if self.allows_list:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing(primary_object)}, {thing(secondary_object)} and {thing(tertiary_object)} {req(self.required_parameter)} {thing(target_object)}")
            else:
                say(f"   Example: {action(self.name)} {thing(primary_object)}, {thing(secondary_object)} and {thing(tertiary_object)}")
        else:
            if self.required_parameter is not None:
                say(f"   Example: {action(self.name)} {thing(primary_object)} {req(self.required_parameter)} {thing(target_object)}")
            else:
                say(f"   Example: {action(self.name)} {thing(primary_object)}")