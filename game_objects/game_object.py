from components.component import Component
from src.grammar import Grammar
from typing import TYPE_CHECKING, Dict
from src.printing import *
from src.state import Physical, Verbs
if TYPE_CHECKING:
    from game import Game

class GameObject:
    def __init__(self, game_instance):
        self._components: Dict[str, Component]= {}
        self._callable_methods: Dict[str, function]= {}
        self._state_list = []
        self.name = ""
        self.game_instance: Game = game_instance
        self.register_callable_method("status", self.status)
        self.register_callable_method("actions", self.list_actions)
        self.position: GameObject = None
        self.flavour_impact = None
        self.property: Physical = Physical.SOLID
        self.spelling = {
            "it": "it",
            "is": "is"
        }

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

    def register_callable_method(self, method_name, method):
        self._callable_methods[method_name] = method

    def try_call_method(self, method_name, with_object = None):
        if method_name in self._callable_methods:
            if with_object:
                self._callable_methods[method_name](with_object)
                return
            self._callable_methods[method_name]()
            return

        # If the method is not found
        warn(f"You cannot {action(method_name)} the {thing(self.name)}")