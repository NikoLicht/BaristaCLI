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
        self._callable_methods: Dict[str, function]= {}
        self.required_words = []
        self._state_list = []
        self.name = ""
        self.game_instance: Game = game_instance
        self.register_callable_method(ActionObject("status", None, False), self.status)
        self.register_callable_method(ActionObject("actions", None, False), self.list_actions)
        self.register_callable_method(ActionObject("put", "into", True), self.put)
        self.position: GameObject = None
        self.flavour_impact = None
        self.property: Physical = Physical.SOLID
        self.spelling = {
            "it": "it",
            "is": "is"
        }

        #implement this dict if anythin particular should happen, when the state is changed.        
        self.property_change_action: Dict[Physical, Callable] = {}


    def status(self):
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


    def list_actions(self):
        action_list = [x for x in self._callable_methods.keys() if x not in ["actions", "status"]]
        grammar = Grammar()
        say(f"{thing(self.name)} has these actions: {grammar.make_list(action_list, style=action)} - but you can always use {action("actions")} and {action("status")}")

    def put(self, into):
        container: Container = into.get_component("container")
        if container:
            container.fill(self)
        else:
            warn(f"You cannot {action('put')} {thing(self.name)} into {thing(into.name)}")

    def AddComponent(self, component: Component) -> Component:
        component.attach_to(self)
        self._components[component.key()] = component
        for key, func in component.get_methods().items():
            if key not in self._callable_methods:
                self._callable_methods[key] = func
        return component

    def get_component(self, name):
        return self._components.get(name.lower())

    def add_state(self, state):
        self._state_list.append(state)
    
    def has_state(self, state):
        return state in self._state_list

    def register_callable_method(self, action_object: ActionObject, method: Callable ):
        self._callable_methods[action_object.name] = method
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

    def try_call_method(self, method_name, with_object = None):
        if method_name in self._callable_methods:
            if with_object:
                self._callable_methods[method_name](with_object)
                return
            self._callable_methods[method_name]()
            return

        # If the method is not found
        warn(f"You cannot {action(method_name)} the {thing(self.name)}")

    def supports_required_word(self, word) -> bool:
        return word in self.required_words
        

    def __str__(self):
        return self.name