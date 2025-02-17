from __future__ import annotations
from components.component import Component
from components.container import Container
from src.grammar import Grammar
from typing import TYPE_CHECKING, Dict
from src.printing import *
from src.state import Physical, Verbs
from collections.abc import Callable
from src.action_object import ActionObject
if TYPE_CHECKING:
    from src.game import Game



class GameObject:
    def __init__(self, game_instance):
        self._components: Dict[str, Component]= {}
        self._game_object_methods: Dict[str, function]= {}
        self.required_words = []
        self._state_list = []
        self.name = ""
        self._lore = None
        self.weight = 120
        self.game_instance: Game = game_instance
        self.register_callable_method(ActionObject("status", None, False, [self.status], [ self ]))
        self.register_callable_method(ActionObject("actions", None, False, [self.list_actions], [ self ]))
        self.register_callable_method(ActionObject("put", "into", True, [self.put], [ self ]))
        self.start_text = None
        self.position: GameObject = None
        self.flavour_impact = None
        self.property: Physical = Physical.SOLID
        self.spelling = {
            "it": "it",
            "is": "is"
        }
        self.print_game_text()

        #implement this dict if anythin particular should happen, when the state is changed.        
        self.property_change_action: Dict[Physical, Callable] = {}


    def status(self):
        """Prints the status of the gameobject and its components."""
        grammar = Grammar()

        #status string
        status_string = "normal"
        if len(self._state_list) > 0:
            status_string = grammar.make_list(self._state_list)
        say(f"{thing(self.name)} is {status_string}.")

        #physical state
        say(f"{thing(self.name)} state is {self.property.name.lower()}.")

        #position string
        position_str = f"{thing(self.name)} {self.spelling["is"]} on the counter."
        if self.position != None:
            position_str = f"{thing(self.name)} {self.spelling["is"]} inside {thing(self.position.name)}."
        say(position_str)
            
        #component status
        for comp in self._components:
            self._components[comp].try_call("status")

    def explanation(self):
        say(self.lore)
        say(f"Use {action("actions")} {thing(self.name)} - to see the applicable actions.")
        say(f"Use {action("status")} {thing(self.name)} - to see the state of the {thing(self.name)}.")

    @property
    def lore(self):
        return self._lore if self._lore else f"It is really just {self.name}."
    
    @lore.setter
    def lore(self, value: str):
        self._lore = value


    def list_actions(self):
        """prints all actions that the game_object has."""
        general_actions = ["status", "actions", "put"]
        action_list = [x for x in self._game_object_methods.keys()]
        component_action_dict = self.get_all_methods() 
        action_list.extend([x for x in component_action_dict.keys()])
        action_list = [x for x in action_list if x not in general_actions]

        grammar = Grammar()
        say(f"   [u]{thing(self.name)} action overview                         [/u]")
        say(f"   General actions: {grammar.make_list(general_actions, style=action)}")

        if len(action_list) > 0:
            say(f"    Unique actions: {grammar.make_list(action_list, style=action)}")

        if self.required_words is not None and len(self.required_words) > 0:
            say(f"          Supports: {grammar.make_list(self.required_words, style=req)}")

    def put(self, into):
        container: Container = into.get_component("container")
        if container:
            container.fill(self)
        else:
            warn(f"You cannot {action('put')} {thing(self.name)} into {thing(into.name)}")

    def AddComponent(self, component: Component) -> Component:
        # Attach the component to the game object
        component.attach_to(self)
        self._components[component.key()] = component

        return component
    
    def print_game_text(self):
        if self.start_text is not None:
            say(self.start_text)

    def get_component(self, name):
        return self._components.get(name.lower())

    def add_state(self, state):
        self._state_list.append(state)
    
    def has_state(self, state):
        return state in self._state_list

    def register_callable_method(self, action_object: ActionObject):
        self._game_object_methods[action_object.name] = action_object
        self.game_instance.register_action(action_object)
    
    def register_required_word(self, word: str):
        if word not in self.required_words:
            self.required_words.append(word)

    def change_property(self, property: Physical) -> None:
        if self.property != property:
            self.property = property

        if property in self.property_change_action.keys():
            if self.property_change_action[property] is not None:
                self.property_change_action[property]()

    def get_all_methods(self):
        joined_methods: Dict[str, ActionObject] = {}
        for comp in self._components:
            methods = self._components[comp].get_methods()
            if methods:
                joined_methods.update(methods)

        for key, value in self._game_object_methods.items():
            if key not in joined_methods:
                joined_methods[key] = value

        return joined_methods


    def try_call_method(self, method_name, target_object = None):
        all_methods: Dict[str, ActionObject] = self.get_all_methods()
        if method_name in all_methods:
            if target_object:
                all_methods[method_name].get_method()(target_object) 
                return
            all_methods[method_name].get_method()()
            return

        # If the method is not found
        warn(f"You cannot {action(method_name)} the {thing(self.name)}")

    def supports_required_word(self, word) -> bool:
        return word in self.required_words
    
    def set_position(self, new_position: GameObject):
        if self.position is not None:
            prev_container: Container = self.position.get_component("container")
            if prev_container:
                prev_container.remove_content(self)
        self.position = new_position
        new_container: Container = new_position.get_component("container")
        if new_container:
            new_container.contains.append(self)
        
    def get_weight(self) -> int:
        """gets the weight in grams of object and all contained objects"""
        container: Container = self.get_component("container")
        total = self.weight
        if container:
            [total := total + x.weight for x in container.get_contents([])]
        return total
        

    def __str__(self):
        return self.name