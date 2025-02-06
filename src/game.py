from game_objects import *
from .CLI import CLI
from .printing import *
from .grammar import Grammar
from typing import Type, List, Dict, TYPE_CHECKING
from .action_object import ActionObject

if TYPE_CHECKING:
    from components import *

class Game:
    def __init__(self):
        self.registered_actions: Dict[str, ActionObject] = {}

        self.CLI = CLI()
        self.CLI.set_game(self)

        self.grammar = Grammar()

        self.objects : Dict[GameObject] = {
            "water" : Water(self),
            "aeropress" : AeroPress(self),
            "beans" : Beans(self),
            "grinder" : Grinder(self),
            "kettle" : Kettle(self),
            "fridge" : Fridge(self),
            "cup": Cup(self),
            "tea": Tea(self)
        }

    def register_action(self, action: ActionObject):
        if action.name not in self.registered_actions:
            self.registered_actions[action.name.lower()] = action
        else:
            self.registered_actions[action.name.lower()].add_action_object(action)

    def perform_action_simple(self, try_action, object: GameObject):
        object.try_call_method(try_action)
    
    def perform_action_complex(self, try_action, object, target : GameObject):
        object.try_call_method(try_action, target)

    def destroy_game_object(self, objects_to_destroy: List[GameObject]):
        warn(f"You won't have access to {self.grammar.make_list(objects_to_destroy, 'or')} anymore.")
        for obj in objects_to_destroy:
            if obj.name.lower() in self.objects:
                container: Container = self.objects[obj.name.lower()].get_component("container")
                if container:
                    for thing in container.contains:
                        thing.position = None
                del self.objects[obj.name.lower()]


    def create_new_game_object(self, name: str, type: Type[GameObject]) -> GameObject:
        self.objects[name] = type(self)
        say(f"{thing(name)} has been added to your objects.")
        return self.objects[name]


    def run(self):
        self.CLI.run()

