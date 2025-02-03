from game_objects import *
from .CLI import CLI
from .printing import *
from .grammar import Grammar
from typing import Type, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from components import *

class Game:
    def __init__(self):

        self.CLI = CLI()
        self.CLI.set_game(self)

        self.grammar = Grammar()

        self.objects : Dict[GameObject] = {
            "water" : Water(self),
            "aeropress" : AeroPress(self),
            "beans" : Beans(self),
            "grinder" : Grinder(self),
            "kettle" : Kettle(self),
            "fridge" : Fridge(self)
        }

    def perform_action_simple(self, try_action, object):
        if object in self.objects:
            self.objects[object].try_call_method(try_action)
        else:
            warn(f"There is no object called {object} - use {action("objects")} to see which {thing("objects")} you can interact with.")
    
    def perform_action_complex(self, try_action, object, second_object : GameObject):
        if object not in self.objects:
            warn(f"There is no object called {object} - use {action("objects")} to see which {thing("objects")} you can interact with.")
            return

        if second_object not in self.objects:
            warn(f"There is no object called {second_object} - use {action("objects")} to see which {thing("objects")} you can interact with.")
            return

        self.objects[second_object].try_call_method(try_action, self.objects[object])

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
        say(f"{thing(name)} has been added to your {action("objects")}.")
        return self.objects[name]


    def run(self):
        self.CLI.run()

