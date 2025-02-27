from __future__ import annotations
from components.component import Component
from components.container import Container
from src.grammar import Grammar
from typing import TYPE_CHECKING, Dict, List
from src.printing import *
from src.state import Physical, Temperature
from collections.abc import Callable
from src.action_object import ActionObject

if TYPE_CHECKING:
    from src.game import Game

from src.coffee_factory import ExtractionResult
class Flavour():
    def __init__(self, taste, amount = 1.0, solubility = 1.0):
        self.taste: str = taste
        self.solubility = solubility
        self.amount: float = amount
    
    def __add__(self, other: Flavour):
        return Flavour(self.taste, self.amount + other.amount, (self.solubility + other.solubility) / 2.0)
        

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
        self.taste: Dict[str, Flavour] = {}
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


    def extract_flavour(self, temp: float, time: int) -> ExtractionResult:
        '''Determines how much flavour is extracted based on parameters'''
        extract = ExtractionResult()
        diffusion: float = self._calc_diffusion()
        for taste_key in self.taste:
            total_extraction: float = 0.0
            amount = self.taste[taste_key].amount
            solubility = self.taste[taste_key].solubility
            time_factor = 1
            decay_speed = 0.05

            #print(f"------- calculating extraction of {taste_key} from {self.name}.")
            #print(f"   amount     | {amount}")
            #print(f"   solubility | {solubility}")
            #print(f"   temp       | {temp}")
            #print(f"   diffusion  | {diffusion}")
            #print(f"")

            for time_step in range(time + 1):
                #print(f">  {time_step}. Iteration _")
                time_factor = 1 / (1 + decay_speed * time_step) # less and less will be extracted
                time_factor = max(time_factor, 0.1) 
                #print(f"   time factor = {round(time_factor, 2)}")
                iteration_sum = amount * solubility * diffusion * temp * time_factor
                #print(f"   this iteration= {round(iteration_sum, 2)}")
                total_extraction += iteration_sum
                #print(f"   total = {round(total_extraction, 2)}")
                #print(f"")
            extract.flavors[taste_key] = total_extraction
        return extract



    def _calc_diffusion(self) -> float:
        if self.property in [Physical.LIQUID, Physical.MUSH]:
            return 1.0
        elif self.property in [Physical.SOLID]:
            return 0.3
        elif self.property in [Physical.SAND]:
            return 0.7
        elif self.property in [Physical.POWDER]:
            return 0.9
        return 0.0


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

    def add_taste(self, taste: str, solubility: float, amount: float):
        self.taste[taste] = Flavour(taste, amount, solubility)


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
    
    def extend_taste(self, taste: Dict[str, Flavour]):
        for key, val in taste.items():
            if key in self.taste:
                self.taste[key] += val
            else:
                self.taste[key] = val


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
    
    def get_flavour_list(self) -> List[str]:
        return [x.taste for x in self.taste]
        

        

    def __str__(self):
        return self.name